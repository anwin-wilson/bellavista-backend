import requests

RAILWAY_URL = "https://bellavista-backend-production.up.railway.app"

print("🚂 TESTING RAILWAY EMAIL")
print("=" * 40)

# Test email configuration
try:
    response = requests.get(f"{RAILWAY_URL}/api/tours/test/", timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Connection: {response.status_code}")
        print(f"📧 Email configured: {data.get('email_configured')}")
        print(f"📊 Total bookings: {data.get('total_bookings')}")
    else:
        print(f"❌ Connection failed: {response.status_code}")
        exit()
except Exception as e:
    print(f"❌ Connection error: {e}")
    exit()

# Test booking with email
booking_data = {
    'first_name': 'Railway',
    'last_name': 'Test',
    'email': 'anwinws@gmail.com',
    'phone_number': '07123456789',
    'preferred_home': 'cardiff',
    'preferred_date': '2025-12-25',
    'preferred_time': '14:00',
    'notes': 'Railway email test'
}

print("\nTesting booking with email...")
try:
    response = requests.post(f"{RAILWAY_URL}/api/tours/book/", json=booking_data, timeout=60)
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Booking created: ID {data.get('booking_id')}")
        print(f"📧 Email sent: {data.get('email_sent')}")
        
        if data.get('email_sent'):
            print("🎉 SUCCESS! Railway email works!")
        else:
            print("⚠️  Email not sent on Railway either")
    else:
        print(f"❌ Booking failed: {response.status_code} - {response.text[:200]}")
except Exception as e:
    print(f"❌ Error: {e}")

print(f"\n📋 COMPARISON:")
print(f"Render:  ✅ API works, ❌ Email blocked (SMTP restrictions)")
print(f"Railway: Testing now...")