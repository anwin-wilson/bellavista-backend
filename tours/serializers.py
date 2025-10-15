# Serializers for Tour Booking API
# Serializers convert between Python objects and JSON for API requests/responses

from rest_framework import serializers
from datetime import date
from .models import TourBooking


class TourBookingSerializer(serializers.ModelSerializer):
    """
    Main serializer for TourBooking model.
    
    This handles the conversion between TourBooking model instances
    and JSON data for API requests and responses.
    """
    
    class Meta:
        model = TourBooking
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'preferred_home', 'preferred_date', 'preferred_time',
            'notes', 'status', 'created_at'
        ]
        # These fields are automatically set and cannot be modified by users
        read_only_fields = ['id', 'created_at']
    
    def validate_preferred_date(self, value):
        """
        Custom validation for preferred_date field.
        Ensures users cannot book tours for past dates.
        """
        # Allow bookings for today and future dates (lenient for timezone issues)
        from datetime import timedelta
        min_date = date.today() - timedelta(days=1)
        if value < min_date:
            raise serializers.ValidationError("Tour date cannot be in the past.")
        return value
    
    def validate_email(self, value):
        """
        Custom validation for email field.
        Ensures email format is valid and converts to lowercase.
        """
        if not value or '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address.")
        return value.lower()


class TourBookingCreateSerializer(TourBookingSerializer):
    """
    Specialized serializer for creating new tour bookings.
    
    Inherits from TourBookingSerializer and adds create method
    for handling new booking creation.
    """
    
    def create(self, validated_data):
        """
        Create a new tour booking with validated data.
        
        Args:
            validated_data (dict): Cleaned and validated booking data
            
        Returns:
            TourBooking: The newly created booking instance
        """
        return TourBooking.objects.create(**validated_data)


class TourBookingListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing tour bookings.
    
    Includes additional computed fields like full_name and
    human-readable home names for better display in lists.
    """
    
    # Computed fields from model properties/methods
    full_name = serializers.ReadOnlyField()
    home_display_name = serializers.CharField(
        source='get_home_display_name', 
        read_only=True
    )
    
    class Meta:
        model = TourBooking
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'preferred_home', 'home_display_name', 'preferred_date', 'preferred_time',
            'notes', 'status', 'created_at'
        ]