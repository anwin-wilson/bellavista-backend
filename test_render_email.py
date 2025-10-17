import requests
import time

RENDER_URL = "https://bellavista-backend-3.onrender.com"

print("📧 Testing Email on Live Render Service")
print("=" * 50)

# Test email functionality
email = input("Enter your email: ").strip()
if not email:
    print("No email provided!")
    exit()

print(f"Sending test email to {email}...")

try:
    start = time.time()
    response = requests.post(
        f"{RENDER_URL}/api/tours/test-connection/",
        json={'email': email},
        timeout=60
    )
    elapsed = time.time() - start
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Response in {elapsed:.2f}s")
        
        if 'email_test' in data:
            email_result = data['email_test']
            if email_result['success']:
                print(f"📧 Email sent successfully!")
                print(f"⏱️  Email time: {email_result['time']}")
            else:
                print(f"❌ Email failed: {email_result['error']}")
        else:
            print("⚠️  No email test data in response")
    else:
        print(f"❌ HTTP {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Request failed: {e}")

print("\n🎯 Creating test booking with email...")

booking_data = {
    'first_name': 'Email',
    'last_name': 'Test',
    'email': email,
    'phone_number': '07123456789',
    'preferred_home': 'cardiff',
    'preferred_date': '2024-12-20',
    'preferred_time': '14:00',
    'notes': 'Email functionality test'
}

try:
    start = time.time()
    response = requests.post(
        f"{RENDER_URL}/api/tours/book/",
        json=booking_data,
        timeout=60
    )
    elapsed = time.time() - start
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Booking created in {elapsed:.2f}s")
        print(f"🆔 Booking ID: {data.get('booking_id')}")
        print(f"📧 Email sent: {data.get('email_sent')}")
    else:
        print(f"❌ Booking failed: {response.status_code} - {response.text}")

except Exception as e:
    print(f"❌ Booking request failed: {e}")