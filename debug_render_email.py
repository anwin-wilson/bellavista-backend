import requests

RENDER_URL = "https://bellavista-backend-3.onrender.com"

print("🔍 DEBUGGING RENDER EMAIL")
print("=" * 40)

# Test email with actual booking
booking_data = {
    'first_name': 'Email',
    'last_name': 'Debug',
    'email': 'anwinws@gmail.com',
    'phone_number': '07123456789',
    'preferred_home': 'cardiff',
    'preferred_date': '2024-12-30',
    'preferred_time': '14:00',
    'notes': 'Email debug test'
}

print("Creating booking with email...")
try:
    response = requests.post(f"{RENDER_URL}/api/tours/book/", json=booking_data, timeout=60)
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Booking created: ID {data.get('booking_id')}")
        print(f"📧 Email sent: {data.get('email_sent')}")
        print(f"📝 Message: {data.get('message')}")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test direct email endpoint
print("\nTesting email endpoint...")
try:
    response = requests.post(
        f"{RENDER_URL}/api/tours/test/",
        json={'email': 'anwinws@gmail.com'},
        timeout=60
    )
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Email test response received")
        if 'email_test' in data:
            email_result = data['email_test']
            print(f"📧 Success: {email_result.get('success')}")
            if not email_result.get('success'):
                print(f"❌ Error: {email_result.get('error')}")
    else:
        print(f"❌ HTTP {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n💡 If email still fails:")
print("1. Redeploy Render service")
print("2. Check environment variable names match exactly")
print("3. Restart Render service")