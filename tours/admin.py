from django.contrib import admin
from .models import TourBooking

@admin.register(TourBooking)
class TourBookingAdmin(admin.ModelAdmin):
    """Admin interface for TourBooking model"""
    
    list_display = [
        'full_name', 'email', 'phone_number', 'preferred_home',
        'preferred_date', 'preferred_time', 'status', 'created_at'
    ]
    
    list_filter = [
        'preferred_home', 'status', 'preferred_date', 'created_at'
    ]
    
    search_fields = [
        'first_name', 'last_name', 'email', 'phone_number'
    ]
    
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Tour Details', {
            'fields': ('preferred_home', 'preferred_date', 'preferred_time')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_visited', 'mark_as_not_visited', 'mark_as_pending']
    
    def mark_as_visited(self, request, queryset):
        """Mark selected bookings as visited"""
        updated = queryset.update(status='visited')
        self.message_user(request, f'{updated} bookings marked as visited.')
    mark_as_visited.short_description = "Mark selected bookings as visited"
    
    def mark_as_not_visited(self, request, queryset):
        """Mark selected bookings as not visited"""
        updated = queryset.update(status='not_visited')
        self.message_user(request, f'{updated} bookings marked as not visited.')
    mark_as_not_visited.short_description = "Mark selected bookings as not visited"
    
    def mark_as_pending(self, request, queryset):
        """Mark selected bookings as pending"""
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} bookings marked as pending.')
    mark_as_pending.short_description = "Mark selected bookings as pending"