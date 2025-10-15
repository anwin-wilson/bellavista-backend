# URL Configuration for Tours App
# Maps URL patterns to view functions for the tour booking system

from django.urls import path
from . import views
from .simple_views import simple_book_tour
from .fast_views import fast_bookings_list, fast_book_tour
from .diagnostic_views import health_check, db_check, minimal_create

# App namespace for URL reversing
app_name = 'tours'

urlpatterns = [
    # =============================================================================
    # MAIN BOOKING ENDPOINTS
    # =============================================================================
    
    # Create new tour booking (POST) or get endpoint info (GET)
    path('book/', views.TourBookingCreateView.as_view(), name='book_tour'),
    
    # List all tour bookings (for admin)
    path('bookings/', views.TourBookingListView.as_view(), name='list_bookings'),
    
    # Update booking status (PATCH)
    path('bookings/<int:booking_id>/status/', views.update_tour_status, name='update_status'),
    
    # Export bookings to Excel
    path('export/', views.export_tours, name='export_tours'),

    # =============================================================================
    # UTILITY ENDPOINTS
    # =============================================================================
    
    # Get available time slots for a date/home
    path('available-slots/', views.available_slots, name='available_slots'),
    
    # Get booking statistics
    path('stats/', views.booking_stats, name='booking_stats'),
    
    # Test API connection
    path('test/', views.test_connection, name='test_connection'),
    
    # Simple booking test
    path('simple-book/', simple_book_tour, name='simple_book'),
    
    # Fast endpoints
    path('fast-bookings/', fast_bookings_list, name='fast_bookings'),
    path('fast-book/', fast_book_tour, name='fast_book'),
    
    # Diagnostic endpoints
    path('health/', health_check, name='health'),
    path('db-check/', db_check, name='db_check'),
    path('minimal-create/', minimal_create, name='minimal_create'),

    # =============================================================================
    # LOCATION SERVICES
    # =============================================================================
    
    # Find nearest care home to user location
    path('find-nearest-home/', views.find_nearest_home, name='find_nearest_home'),
]
