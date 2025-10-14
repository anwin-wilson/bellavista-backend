from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from tours.models import TourBooking


class TourBookingModelTest(TestCase):
    """Test cases for TourBooking model"""

    def setUp(self):
        """Set up test data"""
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

    def test_create_valid_booking(self):
        """Test creating a valid tour booking"""
        booking = TourBooking.objects.create(**self.valid_booking_data)

        self.assertEqual(booking.first_name, 'John')
        self.assertEqual(booking.last_name, 'Doe')
        self.assertEqual(booking.email, 'anwinws@gmail.com')
        self.assertEqual(booking.preferred_home, 'cardiff')
        self.assertEqual(booking.status, 'pending')
        self.assertIsNotNone(booking.created_at)
        self.assertIsNotNone(booking.updated_at)
        self.assertEqual(booking.phone_number, '+1234567890')

    def test_full_name_property(self):
        """Test the full_name property"""
        # With last name
        booking = TourBooking.objects.create(**self.valid_booking_data)
        self.assertEqual(booking.full_name, 'John Doe')

        # Without last name
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
        """Test the get_home_display_name method"""
        booking = TourBooking.objects.create(**self.valid_booking_data)
        self.assertEqual(booking.get_home_display_name(), 'Cardiff')

    def test_string_representation(self):
        """Test the __str__ method"""
        booking = TourBooking.objects.create(**self.valid_booking_data)
        expected_str = f"John Doe - cardiff ({booking.preferred_date})"
        self.assertEqual(str(booking), expected_str)

    def test_ordering(self):
        """Test that bookings are ordered by created_at descending"""
        booking1 = TourBooking.objects.create(**self.valid_booking_data)
        booking2 = TourBooking.objects.create(
            first_name='Jane',
            email='jane@example.com',
            phone_number='+1234567890',
            preferred_home='barry',
            preferred_date=date.today() + timedelta(days=2),
            preferred_time='11:00'
        )

        bookings = list(TourBooking.objects.all())
        self.assertEqual(bookings[0], booking2)  # Most recent first
        self.assertEqual(bookings[1], booking1)

    def test_status_choices(self):
        """Test status field choices"""
        booking = TourBooking.objects.create(**self.valid_booking_data)

        # Test valid statuses
        valid_statuses = ['pending', 'visited', 'not_visited']
        for status in valid_statuses:
            booking.status = status
            booking.save()
            booking.refresh_from_db()
            self.assertEqual(booking.status, status)

    def test_home_choices(self):
        """Test preferred_home field choices"""
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
        """Test that last_name and notes are optional"""
        booking = TourBooking.objects.create(
            first_name='Test',
            email='test@example.com',
            phone_number='+1234567890',
            preferred_home='cardiff',
            preferred_date=date.today() + timedelta(days=1),
            preferred_time='10:00'
        )

        self.assertIsNone(booking.last_name)
        self.assertIsNone(booking.notes)
        self.assertEqual(booking.status, 'pending')
