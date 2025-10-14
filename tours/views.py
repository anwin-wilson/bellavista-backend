from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TourBooking
from .serializers import TourBookingCreateSerializer, TourBookingListSerializer
import requests
import math
from .constants import HOME_LOCATIONS, AVERAGE_SPEED_KMH

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
- Notes: {booking.notes or 'None'}

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

@api_view(['GET'])
def find_nearest_home(request):
    """Find the nearest Bellavista home to a given location"""
    user_location = request.GET.get('location', '').strip()
    user_lat_param = request.GET.get('lat')
    user_lon_param = request.GET.get('lon')

    # Check if required parameters are provided
    if not user_location and not (user_lat_param and user_lon_param):
        return Response({
            'error': 'Location parameter or both lat and lon parameters are required'
        }, status=status.HTTP_400_BAD_REQUEST)

    if user_lat_param and user_lon_param:
        # Use provided coordinates directly
        try:
            user_lat = float(user_lat_param)
            user_lon = float(user_lon_param)
        except ValueError:
            return Response({
                'error': 'Invalid latitude or longitude values'
            }, status=status.HTTP_400_BAD_REQUEST)
    elif user_location:
        # Geocode user location using Nominatim (OpenStreetMap)
        try:
            nominatim_url = 'https://nominatim.openstreetmap.org/search'
            params = {
                'q': user_location,
                'format': 'json',
                'limit': 1,
                'countrycodes': 'gb'  # Limit to UK
            }
            headers = {
                'User-Agent': 'BellavistaCareHomes/1.0'
            }

            response = requests.get(nominatim_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            if not data:
                return Response({
                    'error': 'Location not found. Please try a different address or postcode.'
                }, status=status.HTTP_404_NOT_FOUND)

            user_lat = float(data[0]['lat'])
            user_lon = float(data[0]['lon'])
        except requests.RequestException as e:
            return Response({
                'error': f'Geocoding service error: {str(e)}'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    # Calculate distances to all homes
    nearest_home = None
    min_distance = float('inf')

    for home_key, home_data in HOME_LOCATIONS.items():
        home_lat, home_lon = home_data['coordinates']
        distance = haversine_distance(user_lat, user_lon, home_lat, home_lon)

        if distance < min_distance:
            min_distance = distance
            nearest_home = {
                'key': home_key,
                'name': home_data['name'],
                'address': home_data['address'],
                'phone': home_data['phone'],
                'distance': round(distance, 1),
                'coordinates': home_data['coordinates']
            }

    if not nearest_home:
        return Response({
            'error': 'No homes found'
        }, status=status.HTTP_404_NOT_FOUND)

    # Estimate driving time (rough calculation)
    duration_hours = min_distance / AVERAGE_SPEED_KMH
    duration_minutes = int(duration_hours * 60)

    # Format duration
    if duration_minutes < 60:
        duration_str = f"{duration_minutes} minutes"
    else:
        hours = duration_minutes // 60
        minutes = duration_minutes % 60
        duration_str = f"{hours} hour{'s' if hours > 1 else ''} {minutes} minutes"

    # Create Google Maps navigation URL
    if user_lat_param and user_lon_param:
        # For coordinates, use them directly as origin
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={user_lat},{user_lon}&destination={nearest_home['coordinates'][0]},{nearest_home['coordinates'][1]}"
    else:
        # For text location, use the location string
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={user_location.replace(' ', '+')}&destination={nearest_home['coordinates'][0]},{nearest_home['coordinates'][1]}"

    return Response({
        'nearest_home': nearest_home['name'],
        'address': nearest_home['address'],
        'phone': nearest_home['phone'],
        'distance': f"{nearest_home['distance']} miles",
        'duration': duration_str,
        'maps_url': maps_url,
        'coordinates': nearest_home['coordinates']
    })

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the great circle distance between two points in miles"""
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Earth's radius in miles
    radius_miles = 3959
    distance = radius_miles * c

    return distance
