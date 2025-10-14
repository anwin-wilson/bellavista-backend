from django.test import TestCase
from django.urls import reverse
from django.core import mail
from datetime import date, timedelta
from rest_framework.test import APIClient
from rest_framework import status
from tours.models import TourBooking


class TourBookingViewsTest(TestCase):
    """Test cases for TourBooking views"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.tomorrow = (date.today() + timedelta(days=1)).isoformat()
        self.valid_booking_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': self.tomorrow,
            'preferred_time': '10:00',
            'notes': 'Test booking'
        }

    def test_tour_booking_create_view_get(self):
        """Test GET request to TourBookingCreateView"""
        url = reverse('tours:book_tour')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('methods', response.data)
        self.assertIn('required_fields', response.data)

    def test_tour_booking_create_view_post_valid(self):
        """Test POST request with valid data to TourBookingCreateView"""
        url = reverse('tours:book_tour')
        response = self.client.post(url, self.valid_booking_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('booking_id', response.data)

        # Check that booking was created
        booking = TourBooking.objects.get(id=response.data['booking_id'])
        self.assertEqual(booking.first_name, 'John')
        self.assertEqual(booking.email, 'john.doe@example.com')

    def test_tour_booking_create_view_post_invalid(self):
        """Test POST request with invalid data to TourBookingCreateView"""
        url = reverse('tours:book_tour')
        invalid_data = self.valid_booking_data.copy()
        invalid_data['email'] = 'invalid-email'  # Invalid email

        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])
        self.assertIn('errors', response.data)

    def test_tour_booking_list_view(self):
        """Test TourBookingListView"""
        # Create some test bookings
        TourBooking.objects.create(**{
            'first_name': 'John',
            'email': 'john@example.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time': '10:00'
        })
        TourBooking.objects.create(**{
            'first_name': 'Jane',
            'email': 'jane@example.com',
            'phone_number': '+1987654321',
            'preferred_home': 'barry',
            'preferred_date': date.today() + timedelta(days=2),
            'preferred_time': '14:00'
        })

        url = reverse('tours:list_bookings')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_available_slots_view(self):
        """Test available_slots view"""
        url = reverse('tours:available_slots')

        # Test with valid parameters
        response = self.client.get(url, {'date': self.tomorrow, 'home': 'cardiff'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('available_slots', response.data)
        self.assertIn('date', response.data)
        self.assertIn('home', response.data)

        # Should return all slots initially
        self.assertEqual(len(response.data['available_slots']), 6)

    def test_available_slots_view_missing_params(self):
        """Test available_slots view with missing parameters"""
        url = reverse('tours:available_slots')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_booking_stats_view(self):
        """Test booking_stats view"""
        # Create test bookings
        TourBooking.objects.create(**{
            'first_name': 'John',
            'email': 'john@example.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time': '10:00',
            'status': 'visited'
        })
        TourBooking.objects.create(**{
            'first_name': 'Jane',
            'email': 'jane@example.com',
            'phone_number': '+1987654321',
            'preferred_home': 'barry',
            'preferred_date': date.today() + timedelta(days=2),
            'preferred_time': '14:00',
            'status': 'pending'
        })

        url = reverse('tours:booking_stats')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_bookings'], 2)
        self.assertEqual(response.data['confirmed_bookings'], 1)
        self.assertEqual(response.data['pending_bookings'], 1)
        self.assertIn('Cardiff', response.data['homes_stats'])
        self.assertIn('Barry', response.data['homes_stats'])

    def test_update_tour_status_view(self):
        """Test update_tour_status view"""
        booking = TourBooking.objects.create(**{
            'first_name': 'Test',
            'email': 'test@example.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time': '10:00'
        })

        url = reverse('tours:update_status', kwargs={'booking_id': booking.id})
        response = self.client.patch(url, {'status': 'visited'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['new_status'], 'visited')

        # Check that status was updated
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'visited')

    def test_update_tour_status_view_invalid_status(self):
        """Test update_tour_status view with invalid status"""
        booking = TourBooking.objects.create(**{
            'first_name': 'Test',
            'email': 'test@example.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time': '10:00'
        })

        url = reverse('tours:update_status', kwargs={'booking_id': booking.id})
        response = self.client.patch(url, {'status': 'invalid'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_update_tour_status_view_not_found(self):
        """Test update_tour_status view with non-existent booking"""
        url = reverse('tours:update_status', kwargs={'booking_id': 999})
        response = self.client.patch(url, {'status': 'visited'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data['success'])

    def test_test_connection_view(self):
        """Test test_connection view"""
        # Create a test booking
        TourBooking.objects.create(**{
            'first_name': 'Test',
            'email': 'test@example.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time': '10:00'
        })

        url = reverse('tours:test_connection')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'connected')
        self.assertEqual(response.data['total_bookings'], 1)

    def test_find_nearest_home_view_with_location(self):
        """Test find_nearest_home view with location parameter"""
        url = reverse('tours:find_nearest_home')
        response = self.client.get(url, {'location': 'Cardiff, UK'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('nearest_home', response.data)
        self.assertIn('distance', response.data)
        self.assertIn('maps_url', response.data)

    def test_find_nearest_home_view_with_coordinates(self):
        """Test find_nearest_home view with lat/lon parameters"""
        url = reverse('tours:find_nearest_home')
        response = self.client.get(url, {'lat': '51.4816', 'lon': '-3.1791'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('nearest_home', response.data)
        self.assertIn('distance', response.data)

    def test_find_nearest_home_view_missing_params(self):
        """Test find_nearest_home view with missing parameters"""
        url = reverse('tours:find_nearest_home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
