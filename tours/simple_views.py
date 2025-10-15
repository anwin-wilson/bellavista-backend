from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TourBooking

@api_view(['POST'])
def simple_book_tour(request):
    """Ultra-simple booking endpoint to test database connection"""
    try:
        # Create booking with minimal data
        booking = TourBooking(
            first_name="Test",
            email="test@example.com", 
            phone_number="123",
            preferred_home="cardiff",
            preferred_date="2025-11-20",
            preferred_time="10:00:00"
        )
        booking.save()
        
        return Response({
            'success': True,
            'booking_id': booking.id
        })
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=400)