from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    # Tour booking endpoints
    path('book/', views.TourBookingCreateView.as_view(), name='book_tour'),
    path('bookings/', views.TourBookingListView.as_view(), name='list_bookings'),
    path('bookings/<int:booking_id>/status/', views.update_tour_status, name='update_status'),
    path('export/', views.export_tours, name='export_tours'),
    
    # Utility endpoints
    path('available-slots/', views.available_slots, name='available_slots'),
    path('stats/', views.booking_stats, name='booking_stats'),
    path('test/', views.test_connection, name='test_connection'),
]