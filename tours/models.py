# Tour Booking Models for Bellavista Care Homes

from django.db import models


class TourBooking(models.Model):
    """
    Model to store tour booking requests from potential residents and families.
    
    This model captures all necessary information for scheduling care home tours,
    including personal details, preferred tour times, and booking status.
    """
    
    # =============================================================================
    # CHOICES FOR DROPDOWN FIELDS
    # =============================================================================
    
    HOME_CHOICES = [
        ('cardiff', 'Cardiff'),
        ('barry', 'Barry'),
        ('waverley', 'Waverley'),
        ('college-fields', 'College Fields'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('visited', 'Visited'),
        ('not_visited', 'Not Visited'),
    ]
    
    # =============================================================================
    # PERSONAL INFORMATION FIELDS
    # =============================================================================
    
    first_name = models.CharField(
        max_length=50,
        help_text="Visitor's first name"
    )
    
    last_name = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        help_text="Visitor's last name (optional)"
    )
    
    email = models.EmailField(
        help_text="Contact email address"
    )
    
    phone_number = models.CharField(
        max_length=17,
        help_text="Contact phone number"
    )
    
    # =============================================================================
    # TOUR DETAILS
    # =============================================================================
    
    preferred_home = models.CharField(
        max_length=20, 
        choices=HOME_CHOICES,
        help_text="Which care home to visit"
    )
    
    preferred_date = models.DateField(
        help_text="Preferred tour date"
    )
    
    preferred_time = models.TimeField(
        help_text="Preferred tour time"
    )
    
    # =============================================================================
    # ADDITIONAL INFORMATION
    # =============================================================================
    
    notes = models.TextField(
        blank=True, 
        null=True,
        help_text="Any special requests or notes"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text="Current status of the booking"
    )
    
    # =============================================================================
    # SYSTEM FIELDS (AUTO-MANAGED)
    # =============================================================================
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the booking was created"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the booking was last updated"
    )
    
    # =============================================================================
    # META CONFIGURATION
    # =============================================================================
    
    class Meta:
        ordering = ['-created_at']  # Show newest bookings first
        verbose_name = 'Tour Booking'
        verbose_name_plural = 'Tour Bookings'
    
    # =============================================================================
    # STRING REPRESENTATION
    # =============================================================================
    
    def __str__(self):
        """String representation shown in admin and queries"""
        return f"{self.full_name} - {self.preferred_home} ({self.preferred_date})"
    
    # =============================================================================
    # CUSTOM PROPERTIES AND METHODS
    # =============================================================================
    
    @property
    def full_name(self):
        """Returns the full name of the visitor"""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    def get_home_display_name(self):
        """Returns the human-readable name of the selected care home"""
        return dict(self.HOME_CHOICES)[self.preferred_home]