from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from rest_framework.test import APIClient
from tours.models import TourBooking
from tours.serializers import (
    TourBookingSerializer,
    TourBookingCreateSerializer,
    TourBookingListSerializer
)


class TourBookingSerializerTest(TestCase):
    """Test cases for TourBooking serializers"""

    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        self.valid_booking_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time': '10:00',
            'notes': 'Test booking'
        }
        self.booking = TourBooking.objects.create(**self.valid_booking_data)

    def test_tour_booking_serializer_valid_data(self):
        """Test TourBookingSerializer with valid data"""
        serializer = TourBookingSerializer(self.booking)
        data = serializer.data

        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertEqual(data['preferred_home'], 'cardiff')
        self.assertIn('id', data)
        self.assertIn('created_at', data)

    def test_tour_booking_create_serializer(self):
        """Test TourBookingCreateSerializer"""
        new_booking_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone_number': '+1987654321',
            'preferred_home': 'barry',
            'preferred_date': (date.today() + timedelta(days=2)).isoformat(),
            'preferred_time': '14:00',
            'notes': 'Another test booking'
        }

        serializer = TourBookingCreateSerializer(data=new_booking_data)
        self.assertTrue(serializer.is_valid())

        booking = serializer.save()
        self.assertEqual(booking.first_name, 'Jane')
        self.assertEqual(booking.preferred_home, 'barry')

    def test_tour_booking_list_serializer(self):
        """Test TourBookingListSerializer"""
        serializer = TourBookingListSerializer(self.booking)
        data = serializer.data

        self.assertIn('full_name', data)
        self.assertIn('home_display_name', data)
        self.assertEqual(data['full_name'], 'John Doe')
        self.assertEqual(data['home_display_name'], 'Cardiff')

    def test_email_validation(self):
        """Test email validation in serializer"""
        # Valid email
        valid_data = self.valid_booking_data.copy()
        serializer = TourBookingCreateSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        # Invalid email (no @)
        invalid_data = self.valid_booking_data.copy()
        invalid_data['email'] = 'invalid-email'
        serializer = TourBookingCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

        # Empty email
        invalid_data['email'] = ''
        serializer = TourBookingCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_date_validation(self):
        """Test preferred_date validation"""
        # Future date (valid)
        valid_data = self.valid_booking_data.copy()
        valid_data['preferred_date'] = (date.today() + timedelta(days=1)).isoformat()
        serializer = TourBookingCreateSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())

        # Past date (invalid)
        invalid_data = self.valid_booking_data.copy()
        invalid_data['preferred_date'] = (date.today() - timedelta(days=1)).isoformat()
        serializer = TourBookingCreateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('preferred_date', serializer.errors)

    def test_email_normalization(self):
        """Test that email is normalized to lowercase"""
        data = self.valid_booking_data.copy()
        data['email'] = 'JOHN.DOE@EXAMPLE.COM'

        serializer = TourBookingCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        booking = serializer.save()
        self.assertEqual(booking.email, 'john.doe@example.com')

    def test_read_only_fields(self):
        """Test that read-only fields are not accepted in input"""
        data = self.valid_booking_data.copy()
        data['id'] = 999  # Should be ignored
        data['created_at'] = '2023-01-01T00:00:00Z'  # Should be ignored

        serializer = TourBookingCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        booking = serializer.save()
        self.assertNotEqual(booking.id, 999)
        self.assertNotEqual(str(booking.created_at), '2023-01-01T00:00:00Z')

    def test_required_fields(self):
        """Test that required fields are validated"""
        required_fields = ['first_name', 'email', 'phone_number', 'preferred_home', 'preferred_date', 'preferred_time']

        for field in required_fields:
            data = self.valid_booking_data.copy()
            del data[field]

            serializer = TourBookingCreateSerializer(data=data)
            self.assertFalse(serializer.is_valid())
            self.assertIn(field, serializer.errors)

    def test_optional_fields(self):
        """Test that optional fields work correctly"""
        data = {
            'first_name': 'Test',
            'email': 'test@example.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': (date.today() + timedelta(days=1)).isoformat(),
            'preferred_time': '10:00'
            # last_name and notes are optional
        }

        serializer = TourBookingCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        booking = serializer.save()
        self.assertIsNone(booking.last_name)
        self.assertIsNone(booking.notes)
