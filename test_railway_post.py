import requests

RAILWAY_URL = "https://bellavista-backend-production.up.railway.app"

print("🔧 TESTING RAILWAY POST ISSUE")
print("=" * 40)

# Test with minimal data first
minimal_booking = {
    'first_name': 'Test',
    'email': 'test@example.com',
    'phone_number': '07123456789',
    'preferred_home': 'cardiff',
    'preferred_date': '2025-01-20',
    'preferred_time': '14:00'
}

print("Testing minimal POST request...")
try:
    response = requests.post(
        f"{RAILWAY_URL}/api/tours/book/", 
        json=minimal_booking, 
        timeout=30
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print(f"\n💡 If this fails, Railway has POST handling issues")
print(f"   Solution: Redeploy Railway from GitHub")