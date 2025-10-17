import requests

RENDER_URL = "https://bellavista-backend-3.onrender.com"

print("🔧 Testing Render Email Fix")
print("=" * 40)

# Test correct endpoint
print("1. Testing correct endpoint...")
try:
    response = requests.get(f"{RENDER_URL}/api/tours/test/", timeout=30)
    print(f"✅ /api/tours/test/ - Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"📧 Email configured: {data.get('email_configured', False)}")
except Exception as e:
    print(f"❌ Failed: {e}")

# Test email via correct endpoint
email = input("\nEnter email for test: ").strip()
if email:
    print(f"2. Testing email via /api/tours/test/...")
    try:
        response = requests.post(
            f"{RENDER_URL}/api/tours/test/",
            json={'email': email},
            timeout=60
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received")
            if 'email_test' in data:
                email_result = data['email_test']
                if email_result['success']:
                    print(f"📧 Email sent successfully!")
                else:
                    print(f"❌ Email failed: {email_result['error']}")
        else:
            print(f"❌ HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Failed: {e}")

print("\n💡 Email might not be configured on Render")
print("   Check Render environment variables!")