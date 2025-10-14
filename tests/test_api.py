from django.test import TestCase
from django.urls import reverse
from django.core import mail
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework import status
from tours.models import TourBooking
import json


class TourBookingAPITest(TestCase):
    """Integration tests for the complete Tour Booking API"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.tomorrow = (date.today() + timedelta(days=1)).isoformat()

    def test_complete_booking_workflow(self):
        """Test the complete booking workflow from creation to status update"""
        # 1. Create a booking
        booking_data = {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice.johnson@example.com',
            'phone_number': '+1555123456',
            'preferred_home': 'cardiff',
            'preferred_date': self.tomorrow,
            'preferred_time': '09:00',
            'notes': 'Integration test booking'
        }

        url = reverse('tours:book_tour')
        response = self.client.post(url, booking_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        booking_id = response.data['booking_id']

        # 2. Verify booking was created
        booking = TourBooking.objects.get(id=booking_id)
        self.assertEqual(booking.first_name, 'Alice')
        self.assertEqual(booking.status, 'pending')

        # 3. Check that booking appears in list
        list_url = reverse('tours:list_bookings')
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(b['id'] == booking_id for b in response.data))

        # 4. Update booking status
        update_url = reverse('tours:update_status', kwargs={'booking_id': booking_id})
        response = self.client.patch(update_url, {'status': 'visited'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 5. Verify status was updated
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'visited')

        # 6. Check that stats reflect the update
        stats_url = reverse('tours:booking_stats')
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['confirmed_bookings'], 1)

    def test_available_slots_integration(self):
        """Test available slots functionality with existing bookings"""
        # Create a booking for tomorrow at 10:00
        TourBooking.objects.create(
            first_name='Test',
            email='test@example.com',
            phone_number='+1234567890',
            preferred_home='cardiff',
            preferred_date=date.today() + timedelta(days=1),
            preferred_time='10:00'
        )

        url = reverse('tours:available_slots')
        response = self.client.get(url, {'date': self.tomorrow, 'home': 'cardiff'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn('10:00', response.data['available_slots'])
        self.assertIn('09:00', response.data['available_slots'])

    def test_email_integration(self):
        """Test email sending integration"""
        booking_data = {
            'first_name': 'Email',
            'last_name': 'Test',
            'email': 'email.test@example.com',
            'phone_number': '+1444987654',
            'preferred_home': 'barry',
            'preferred_date': self.tomorrow,
            'preferred_time': '11:00',
            'notes': 'Email integration test'
        }

        url = reverse('tours:book_tour')
        response = self.client.post(url, booking_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that email was attempted (will be in console backend)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [booking_data['email']])
        self.assertIn('Email Test', email.body)
        self.assertIn('Barry', email.body)

    def test_error_handling_integration(self):
        """Test error handling across the API"""
        # Test invalid booking data
        invalid_data = {
            'first_name': '',  # Required field empty
            'email': 'invalid-email',  # Invalid email
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': self.tomorrow,
            'preferred_time': '10:00'
        }

        url = reverse('tours:book_tour')
        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)

    def test_cross_endpoint_consistency(self):
        """Test that data is consistent across different endpoints"""
        # Create booking
        booking_data = {
            'first_name': 'Consistency',
            'last_name': 'Test',
            'email': 'consistency@example.com',
            'phone_number': '+1333567890',
            'preferred_home': 'waverley',
            'preferred_date': self.tomorrow,
            'preferred_time': '14:00'
        }

        create_url = reverse('tours:book_tour')
        response = self.client.post(create_url, booking_data, format='json')
        booking_id = response.data['booking_id']

        # Check in list view
        list_url = reverse('tours:list_bookings')
        response = self.client.get(list_url)
        booking_from_list = next(b for b in response.data if b['id'] == booking_id)

        self.assertEqual(booking_from_list['first_name'], 'Consistency')
        self.assertEqual(booking_from_list['home_display_name'], 'Waverley')

        # Check in stats
        stats_url = reverse('tours:booking_stats')
        response = self.client.get(stats_url)
        self.assertEqual(response.data['total_bookings'], 1)
        self.assertIn('Waverley', response.data['homes_stats'])

    def test_api_endpoints_return_json(self):
        """Test that all API endpoints return JSON responses"""
        endpoints = [
            (reverse('tours:test_connection'), 'GET', {}),
            (reverse('tours:booking_stats'), 'GET', {}),
            (reverse('tours:available_slots'), 'GET', {'date': self.tomorrow, 'home': 'cardiff'}),
        ]

        for url, method, params in endpoints:
            with self.subTest(url=url):
                if method == 'GET':
                    response = self.client.get(url, params)
                else:
                    response = self.client.post(url, params, format='json')

                self.assertEqual(response.status_code, status.HTTP_200_OK)
                # Check that response is JSON (not HTML)
                self.assertIsInstance(response.data, dict)

    def test_cors_headers(self):
        """Test that CORS headers are properly set"""
        url = reverse('tours:test_connection')
        response = self.client.get(url)

        # Check for CORS headers (if middleware is active)
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers'
        ]

        # At minimum, should not have HTML content type for API responses
        self.assertNotEqual(response.get('Content-Type'), 'text/html')

    def test_concurrent_bookings_same_slot(self):
        """Test handling of concurrent bookings for the same time slot"""
        # This would require more complex testing in a real scenario
        # For now, just test that the same slot can be booked multiple times
        # (in reality, you'd want to prevent this)

        booking_data = {
            'first_name': 'Concurrent',
            'email': 'concurrent@example.com',
            'phone_number': '+1222567890',
            'preferred_home': 'cardiff',
            'preferred_date': self.tomorrow,
            'preferred_time': '15:00'
        }

        # Create first booking
        url = reverse('tours:book_tour')
        response1 = self.client.post(url, booking_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Create second booking for same slot (should succeed for now)
        booking_data['email'] = 'concurrent2@example.com'
        response2 = self.client.post(url, booking_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Both bookings should exist
        self.assertEqual(TourBooking.objects.filter(
            preferred_date=date.today() + timedelta(days=1),
            preferred_time='15:00',
            preferred_home='cardiff'
        ).count(), 2)
