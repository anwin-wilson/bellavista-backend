from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TourBooking
from .serializers import TourBookingCreateSerializer, TourBookingListSerializer

class TourBookingCreateView(generics.CreateAPIView):
    """API view to create a new tour booking"""
    
    queryset = TourBooking.objects.all()
    serializer_class = TourBookingCreateSerializer
    
    def get(self, request, *args, **kwargs):
        """Handle GET requests - return form schema or empty response"""
        return Response({
            'message': 'Tour booking endpoint ready',
            'methods': ['POST'],
            'required_fields': ['first_name', 'last_name', 'email', 'phone_number', 'preferred_home', 'preferred_date', 'preferred_time']
        })
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            booking = serializer.save()
            
            # Try to send confirmation email
            email_sent = self.send_confirmation_email(booking)
            
            return Response({
                'success': True,
                'message': 'Tour booking submitted successfully!',
                'booking_id': booking.id,
                'email_sent': email_sent
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Please check the form for errors.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def send_confirmation_email(self, booking):
        """Send confirmation email to customer"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        try:
            subject = f'Tour Booking Confirmation - #{booking.id}'
            
            message = f"""
Dear {booking.first_name},

Thank you for booking a tour with Bellavista Care Homes!

Booking Details:
- Booking ID: #{booking.id}
- Name: {booking.full_name}
- Location: {booking.get_home_display_name()}
- Date: {booking.preferred_date.strftime('%B %d, %Y')}
- Time: {booking.preferred_time.strftime('%I:%M %p')}
- Phone: {booking.phone_number}
- Special Requirements: {booking.special_requirements or 'None'}

We will contact you within 24 hours to confirm your tour details.

Best regards,
Bellavista Care Homes Team
"""
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [booking.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f'Email sending failed: {e}')
            return False

class TourBookingListView(generics.ListAPIView):
    """API view to list all tour bookings (for admin)"""
    
    queryset = TourBooking.objects.all()
    serializer_class = TourBookingListSerializer
    


@api_view(['GET'])
def available_slots(request):
    """API endpoint to get available time slots for a specific date and home"""
    date = request.GET.get('date')
    home = request.GET.get('home')
    
    if not date or not home:
        return Response({
            'error': 'Date and home parameters are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    existing_bookings = TourBooking.objects.filter(
        preferred_date=date,
        preferred_home=home
    ).values_list('preferred_time', flat=True)
    
    all_slots = ['09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
    available_slots = [
        slot for slot in all_slots 
        if slot not in [str(time) for time in existing_bookings]
    ]
    
    return Response({
        'available_slots': available_slots,
        'date': date,
        'home': home
    })

@api_view(['GET'])
def booking_stats(request):
    """API endpoint to get booking statistics"""
    total_bookings = TourBooking.objects.count()
    confirmed_bookings = TourBooking.objects.filter(is_confirmed=True).count()
    pending_bookings = total_bookings - confirmed_bookings
    
    homes_stats = {}
    for home_code, home_name in TourBooking.HOME_CHOICES:
        count = TourBooking.objects.filter(preferred_home=home_code).count()
        homes_stats[home_name] = count
    
    return Response({
        'total_bookings': total_bookings,
        'confirmed_bookings': confirmed_bookings,
        'pending_bookings': pending_bookings,
        'homes_stats': homes_stats
    })

@api_view(['PATCH'])
def update_tour_status(request, booking_id):
    """Update tour booking status"""
    try:
        booking = TourBooking.objects.get(id=booking_id)
        status = request.data.get('status')
        
        if status in ['visited', 'not_visited', 'pending']:
            booking.status = status
            booking.save()
            return Response({
                'success': True,
                'message': f'Status updated to {status}',
                'booking_id': booking_id,
                'new_status': status
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid status'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except TourBooking.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def export_tours(request):
    """Export tour bookings to Excel"""
    try:
        import pandas as pd
        from django.http import HttpResponse
        import io
        
        status = request.GET.get('status', 'all')
        
        # Filter bookings based on status
        if status == 'all':
            bookings = TourBooking.objects.all()
        else:
            bookings = TourBooking.objects.filter(status=status)
        
        # Convert to DataFrame
        data = []
        for booking in bookings:
            data.append({
                'ID': booking.id,
                'First Name': booking.first_name,
                'Last Name': booking.last_name or '',
                'Email': booking.email,
                'Phone': booking.phone_number,
                'Location': booking.get_home_display_name(),
                'Date': booking.preferred_date.strftime('%Y-%m-%d'),
                'Time': booking.preferred_time.strftime('%H:%M'),
                'Notes': booking.notes or '',
                'Status': booking.status.title(),
                'Created': booking.created_at.strftime('%Y-%m-%d %H:%M')
            })
        
        df = pd.DataFrame(data)
        
        # Create Excel file
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Tour Bookings', index=False)
        
        output.seek(0)
        
        response = HttpResponse(
            output.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="tour_bookings_{status}.xlsx"'
        
        return response
        
    except ImportError:
        return Response({
            'error': 'Excel export not available. Install pandas and openpyxl.'
        }, status=500)
    except Exception as e:
        return Response({
            'error': f'Export failed: {str(e)}'
        }, status=500)

@api_view(['GET'])
def test_connection(request):
    """Test endpoint to verify frontend-backend connection"""
    return Response({
        'status': 'connected',
        'message': 'Backend is working!',
        'total_bookings': TourBooking.objects.count()
    })