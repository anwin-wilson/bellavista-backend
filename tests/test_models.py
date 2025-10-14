# Test Cases for TourBooking Model
# This file contains unit tests to ensure the TourBooking model works correctly

from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from tours.models import TourBooking


class TourBookingModelTest(TestCase):
    """
    Test suite for the TourBooking model.
    
    Tests all model functionality including:
    - Creating valid bookings
    - Model properties and methods
    - Field validation
    - Model ordering
    """

    def setUp(self):
        """
        Set up test data that will be used across multiple test methods.
        This runs before each individual test method.
        """
        self.valid_booking_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'anwinws@gmail.com',
            'phone_number': '+1234567890',
            'preferred_home': 'cardiff',
            'preferred_date': date.today() + timedelta(days=1),
            'preferred_time': '10:00',
            'notes': 'Test booking'
        }

    # =========================================================================
    # BASIC MODEL FUNCTIONALITY TESTS
    # =========================================================================

    def test_create_valid_booking(self):
        """
        Test creating a valid tour booking with all required fields.
        Verifies that all fields are saved correctly and defaults are applied.
        """
        booking = TourBooking.objects.create(**self.valid_booking_data)

        # Test that all fields are saved correctly
        self.assertEqual(booking.first_name, 'John')
        self.assertEqual(booking.last_name, 'Doe')
        self.assertEqual(booking.email, 'anwinws@gmail.com')
        self.assertEqual(booking.preferred_home, 'cardiff')
        self.assertEqual(booking.phone_number, '+1234567890')
        
        # Test default values
        self.assertEqual(booking.status, 'pending')
        
        # Test auto-generated fields
        self.assertIsNotNone(booking.created_at)
        self.assertIsNotNone(booking.updated_at)

    # =========================================================================
    # MODEL PROPERTIES AND METHODS TESTS
    # =========================================================================

    def test_full_name_property(self):
        """
        Test the full_name property works correctly.
        Should combine first and last name, or just return first name if no last name.
        """
        # Test with both first and last name
        booking = TourBooking.objects.create(**self.valid_booking_data)
        self.assertEqual(booking.full_name, 'John Doe')

        # Test with only first name (last name is optional)
        booking_no_last = TourBooking.objects.create(
            first_name='Jane',
            email='jane@example.com',
            phone_number='+1234567890',
            preferred_home='cardiff',
            preferred_date=date.today() + timedelta(days=1),
            preferred_time='10:00'
        )
        self.assertEqual(booking_no_last.full_name, 'Jane')

    def test_home_display_name_method(self):
        """
        Test the get_home_display_name method.
        Should return the human-readable name for the selected care home.
        """
        booking = TourBooking.objects.create(**self.valid_booking_data)
        self.assertEqual(booking.get_home_display_name(), 'Cardiff')

    def test_string_representation(self):
        """
        Test the __str__ method returns a meaningful string representation.
        This is what appears in Django admin and when printing the object.
        """
        booking = TourBooking.objects.create(**self.valid_booking_data)
        expected_str = f"John Doe - cardiff ({booking.preferred_date})"
        self.assertEqual(str(booking), expected_str)

    # =========================================================================
    # MODEL CONFIGURATION TESTS
    # =========================================================================

    def test_ordering(self):
        """
        Test that bookings are ordered by created_at in descending order.
        Newest bookings should appear first in queries.
        """
        # Create first booking
        booking1 = TourBooking.objects.create(**self.valid_booking_data)
        
        # Create second booking (will have later created_at)
        booking2 = TourBooking.objects.create(
            first_name='Jane',
            email='jane@example.com',
            phone_number='+1234567890',
            preferred_home='barry',
            preferred_date=date.today() + timedelta(days=2),
            preferred_time='11:00'
        )

        # Verify ordering (newest first)
        bookings = list(TourBooking.objects.all())
        self.assertEqual(bookings[0], booking2)  # Most recent first
        self.assertEqual(bookings[1], booking1)

    # =========================================================================
    # FIELD VALIDATION TESTS
    # =========================================================================

    def test_status_choices(self):
        """
        Test that all valid status choices work correctly.
        The status field should accept only predefined values.
        """
        booking = TourBooking.objects.create(**self.valid_booking_data)

        # Test all valid status values
        valid_statuses = ['pending', 'visited', 'not_visited']
        for status in valid_statuses:
            booking.status = status
            booking.save()
            booking.refresh_from_db()
            self.assertEqual(booking.status, status)

    def test_home_choices(self):
        """
        Test that all valid care home choices work correctly.
        The preferred_home field should accept only predefined care homes.
        """
        valid_homes = ['cardiff', 'barry', 'waverley', 'college-fields']

        for home in valid_homes:
            booking = TourBooking.objects.create(
                first_name='Test',
                email=f'test{home}@example.com',
                phone_number='+1234567890',
                preferred_home=home,
                preferred_date=date.today() + timedelta(days=1),
                preferred_time='10:00'
            )
            self.assertEqual(booking.preferred_home, home)

    def test_optional_fields(self):
        """
        Test that optional fields can be left empty.
        Some fields like last_name and notes should be optional.
        """
        booking = TourBooking.objects.create(
            first_name='Test',
            email='test@example.com',
            phone_number='+1234567890',
            preferred_home='cardiff',
            preferred_date=date.today() + timedelta(days=1),
            preferred_time='10:00'
        )

        # Verify optional fields can be None
        self.assertIsNone(booking.last_name)
        self.assertIsNone(booking.notes)
        
        # Verify default status is still applied
        self.assertEqual(booking.status, 'pending')
