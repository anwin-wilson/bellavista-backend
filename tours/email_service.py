"""
SendGrid Email Service for Bellavista Care Homes
HTTP-based email that works on Render free tier
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def send_booking_confirmation_email(booking):
    """
    Send booking confirmation email via SendGrid API
    
    Args:
        booking: TourBooking instance
        
    Returns:
        bool: True if sent successfully, False otherwise
    """
    
    # Check if SendGrid is configured
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        print("SendGrid API key not configured")
        return False
    
    try:
        # Create email content
        subject = f'Tour Booking Confirmation - #{booking.id}'
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #2c3e50;">Tour Booking Confirmation</h2>
            
            <p>Dear {booking.first_name},</p>
            
            <p>Thank you for booking a tour with Bellavista Care Homes!</p>
            
            <div style="background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Booking Details:</h3>
                <p><strong>Booking ID:</strong> #{booking.id}</p>
                <p><strong>Name:</strong> {booking.full_name}</p>
                <p><strong>Location:</strong> {booking.get_home_display_name()}</p>
                <p><strong>Date:</strong> {booking.preferred_date}</p>
                <p><strong>Time:</strong> {booking.preferred_time}</p>
                <p><strong>Phone:</strong> {booking.phone_number}</p>
                <p><strong>Notes:</strong> {booking.notes or 'None'}</p>
            </div>
            
            <p>We will contact you within 24 hours to confirm your tour details.</p>
            
            <p>Best regards,<br>
            <strong>Bellavista Care Homes Team</strong></p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="font-size: 12px; color: #666;">
                This is an automated confirmation email. Please do not reply to this email.
            </p>
        </div>
        """
        
        # Create SendGrid message
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=booking.email,
            subject=subject,
            html_content=html_content
        )
        
        # Send email
        sg = SendGridAPIClient(api_key=sendgrid_api_key)
        response = sg.send(message)
        
        print(f'SendGrid email sent successfully to {booking.email}')
        print(f'Response status: {response.status_code}')
        
        return True
        
    except Exception as e:
        print(f'SendGrid email sending failed: {e}')
        return False

def send_test_email(email_address):
    """
    Send test email via SendGrid
    
    Args:
        email_address: Email to send test to
        
    Returns:
        dict: Result with success status and details
    """
    
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        return {
            'success': False,
            'error': 'SendGrid API key not configured'
        }
    
    try:
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=email_address,
            subject='Bellavista Care Homes - Email Test',
            html_content="""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #2c3e50;">Email Test Successful!</h2>
                <p>This is a test email from Bellavista Care Homes API.</p>
                <p>If you received this email, SendGrid integration is working correctly!</p>
                <p>Best regards,<br><strong>Bellavista Care Homes Team</strong></p>
            </div>
            """
        )
        
        sg = SendGridAPIClient(api_key=sendgrid_api_key)
        response = sg.send(message)
        
        return {
            'success': True,
            'status_code': response.status_code,
            'sent_to': email_address
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }