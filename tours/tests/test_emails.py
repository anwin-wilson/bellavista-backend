from django.test import TestCase
from django.core import mail
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import date, timedelta
import json
from tours.models import TourBooking

class EmailTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        # Convert tomorrow's date to the format used in the email
        self.formatted_date = (date.today() + timedelta(days=1)).strftime('%B %d, %Y')

    def test_booking_email(self):
        # Test data with correct home choice from model
        booking_data = {
            "first_name": "Test User",
            "last_name": "Smith",
            "email": "test@example.com",
            "phone_number": "+1234567890",
            "preferred_home": "cardiff",
            "preferred_date": self.tomorrow,
            "preferred_time": "09:00",
            "notes": "Test booking"
        }

        # Make booking request
        response = self.client.post(
            reverse('tours:book_tour'), 
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        # Print response details for debugging
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.content.decode()}")
        
        # Check response status
        self.assertEqual(response.status_code, 201)
        
        # Check if email was sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Check email content
        email = mail.outbox[0]
        self.assertEqual(email.to, [booking_data['email']])
        self.assertIn(booking_data['first_name'], email.body)
        self.assertIn(self.formatted_date, email.body)  # Using formatted date
        
        # Additional assertions to verify full email content
        self.assertIn('Thank you for booking a tour with Bellavista Care Homes!', email.body)
        self.assertIn(f"Name: {booking_data['first_name']} {booking_data['last_name']}", email.body)
        self.assertIn('Location: Cardiff', email.body)
        self.assertIn('09:00 AM', email.body)