from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import TourBooking

@api_view(['GET'])
def fast_bookings_list(request):
    """Ultra-fast bookings list without serializer overhead"""
    try:
        bookings = TourBooking.objects.all().order_by('-created_at')[:50]  # Limit to 50 recent
        
        data = []
        for booking in bookings:
            data.append({
                'id': booking.id,
                'first_name': booking.first_name,
                'last_name': booking.last_name or '',
                'email': booking.email,
                'phone_number': booking.phone_number,
                'preferred_home': booking.preferred_home,
                'preferred_date': str(booking.preferred_date),
                'preferred_time': str(booking.preferred_time),
                'notes': booking.notes or '',
                'status': booking.status,
                'created_at': booking.created_at.isoformat()
            })
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def fast_book_tour(request):
    """Ultra-fast booking creation"""
    try:
        booking = TourBooking.objects.create(
            first_name=request.data.get('first_name', ''),
            last_name=request.data.get('last_name', ''),
            email=request.data.get('email', ''),
            phone_number=request.data.get('phone_number', ''),
            preferred_home=request.data.get('preferred_home', 'cardiff'),
            preferred_date=request.data.get('preferred_date'),
            preferred_time=request.data.get('preferred_time'),
            notes=request.data.get('notes', ''),
            status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'booking_id': booking.id,
            'message': 'Booking created successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)