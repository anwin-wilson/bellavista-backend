from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import TourBooking
import time

@api_view(['GET'])
def health_check(request):
    """Ultra-minimal health check"""
    return JsonResponse({'status': 'ok', 'timestamp': time.time()})

@api_view(['GET']) 
def db_check(request):
    """Check database connectivity"""
    try:
        count = TourBooking.objects.count()
        return JsonResponse({'db_status': 'ok', 'count': count})
    except Exception as e:
        return JsonResponse({'db_status': 'error', 'error': str(e)})

@api_view(['POST'])
def minimal_create(request):
    """Minimal booking creation test"""
    try:
        booking = TourBooking(
            first_name="Test",
            email="test@test.com",
            phone_number="123",
            preferred_home="cardiff",
            preferred_date="2025-11-25",
            preferred_time="10:00:00"
        )
        booking.save()
        return JsonResponse({'success': True, 'id': booking.id})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})