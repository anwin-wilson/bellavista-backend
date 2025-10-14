# Django Admin Configuration for Tour Booking System
# This file customizes how the TourBooking model appears in Django Admin

from django.contrib import admin
from .models import TourBooking


@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    """
    Custom admin interface for TourBooking model.
    
    This configuration makes it easy for staff to manage tour bookings
    through Django's admin interface with filtering, searching, and bulk actions.
    """
    
    # =============================================================================
    # LIST VIEW CONFIGURATION
    # =============================================================================
    
    # Columns to display in the booking list
    list_display = [
        'full_name', 'email', 'phone_number', 'preferred_home',
        'preferred_date', 'preferred_time', 'status', 'created_at'
    ]
    
    # Filters available in the right sidebar
    list_filter = [
        'preferred_home',  # Filter by care home
        'status',          # Filter by booking status
        'preferred_date',  # Filter by tour date
        'created_at'       # Filter by when booking was made
    ]
    
    # Fields that can be searched
    search_fields = [
        'first_name', 'last_name', 'email', 'phone_number'
    ]
    
    # Fields that cannot be edited (auto-managed by system)
    readonly_fields = ['created_at', 'updated_at']
    
    # =============================================================================
    # DETAIL VIEW CONFIGURATION
    # =============================================================================
    
    # Organize fields into logical sections
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number'),
            'description': 'Contact details for the visitor'
        }),
        ('Tour Details', {
            'fields': ('preferred_home', 'preferred_date', 'preferred_time'),
            'description': 'When and where the tour will take place'
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'description': 'Any special requests or notes'
        }),
        ('Status', {
            'fields': ('status',),
            'description': 'Current status of the booking'
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),  # Collapsed by default
            'description': 'Automatically managed timestamps'
        }),
    )
    
    # =============================================================================
    # BULK ACTIONS
    # =============================================================================
    
    # Custom actions available in the dropdown
    actions = ['mark_as_visited', 'mark_as_not_visited', 'mark_as_pending']
    
    def mark_as_visited(self, request, queryset):
        """
        Bulk action to mark selected bookings as visited.
        
        This is useful when processing multiple completed tours at once.
        """
        updated = queryset.update(status='visited')
        self.message_user(request, f'{updated} bookings marked as visited.')
    mark_as_visited.short_description = "Mark selected bookings as visited"
    
    def mark_as_not_visited(self, request, queryset):
        """
        Bulk action to mark selected bookings as not visited.
        
        Use this for no-shows or cancelled tours.
        """
        updated = queryset.update(status='not_visited')
        self.message_user(request, f'{updated} bookings marked as not visited.')
    mark_as_not_visited.short_description = "Mark selected bookings as not visited"
    
    def mark_as_pending(self, request, queryset):
        """
        Bulk action to reset selected bookings to pending status.
        
        Useful for rescheduled tours or status corrections.
        """
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} bookings marked as pending.')
    mark_as_pending.short_description = "Mark selected bookings as pending"