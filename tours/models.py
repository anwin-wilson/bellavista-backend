from django.db import models
from django.core.validators import RegexValidator

class TourBooking(models.Model):
    """Model for tour booking requests"""
    
    # Personal Information
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=17)
    
    # Tour Details
    HOME_CHOICES = [
        ('cardiff', 'Cardiff'),
        ('barry', 'Barry'),
        ('waverley', 'Waverley'),
        ('college-fields', 'College Fields'),
    ]
    
    preferred_home = models.CharField(max_length=20, choices=HOME_CHOICES)
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    
    # Additional Information
    notes = models.TextField(blank=True, null=True)
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('visited', 'Visited'),
        ('not_visited', 'Not Visited'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Tour Booking'
        verbose_name_plural = 'Tour Bookings'
    
    def __str__(self):
        return f"{self.full_name} - {self.preferred_home} ({self.preferred_date})"
    
    @property
    def full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    def get_home_display_name(self):
        return dict(self.HOME_CHOICES)[self.preferred_home]