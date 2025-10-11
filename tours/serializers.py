from rest_framework import serializers
from .models import TourBooking
from datetime import date, datetime

class TourBookingSerializer(serializers.ModelSerializer):
    """Serializer for TourBooking model"""
    
    class Meta:
        model = TourBooking
        fields = [
            'id', 'first_name', 'last_name', 'email', 'phone_number',
            'preferred_home', 'preferred_date', 'preferred_time',
            'notes', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def validate_preferred_date(self, value):
        """Validate that the preferred date is not in the past"""
        if value < date.today():
            raise serializers.ValidationError("Tour date cannot be in the past.")
        return value
    
    def validate_email(self, value):
        """Validate email format"""
        if not value or '@' not in value:
            raise serializers.ValidationError("Please provide a valid email address.")
        return value.lower()

class TourBookingCreateSerializer(TourBookingSerializer):
    """Serializer for creating tour bookings with additional validation"""
    
    def create(self, validated_data):
        """Create a new tour booking"""
        return TourBooking.objects.create(**validated_data)

class TourBookingListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing tour bookings"""
    
    full_name = serializers.ReadOnlyField()
    home_display_name = serializers.CharField(source='get_home_display_name', read_only=True)
    
    class Meta:
        model = TourBooking
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'preferred_home', 'home_display_name', 'preferred_date', 'preferred_time',
            'notes', 'status', 'created_at'
        ]