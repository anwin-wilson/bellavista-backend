import requests
import time

RAILWAY_URL = "https://bellavista-backend-production.up.railway.app"

print("🔧 DIAGNOSING RAILWAY ISSUES")
print("=" * 40)

# Test different endpoints to see what works
endpoints = [
    "/",
    "/api/",
    "/api/tours/",
    "/api/tours/stats/",
    "/api/tours/test/"
]

for endpoint in endpoints:
    try:
        print(f"Testing {endpoint}...")
        response = requests.get(f"{RAILWAY_URL}{endpoint}", timeout=10)
        print(f"  ✅ {response.status_code}")
    except Exception as e:
        print(f"  ❌ {str(e)[:50]}...")

# Test simple GET request
print(f"\nTesting basic stats endpoint...")
try:
    response = requests.get(f"{RAILWAY_URL}/api/tours/stats/", timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Stats work: {data.get('total_bookings')} bookings")
    else:
        print(f"❌ Stats failed: {response.status_code}")
except Exception as e:
    print(f"❌ Stats error: {e}")

print(f"\n💡 Railway Issues:")
print(f"1. App might be crashing on POST requests")
print(f"2. Environment variables not set")
print(f"3. Database issues")
print(f"4. Memory/timeout problems")

print(f"\n🔧 To fix Railway:")
print(f"1. Check Railway logs for crash details")
print(f"2. Add environment variables")
print(f"3. Redeploy from GitHub")
print(f"4. Check Railway dashboard for errors")