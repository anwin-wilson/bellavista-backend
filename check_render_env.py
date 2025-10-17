import requests

RENDER_URL = "https://bellavista-backend-3.onrender.com"

print("🔍 CHECKING RENDER ENVIRONMENT")
print("=" * 40)

# Check what the server sees for email config
try:
    response = requests.get(f"{RENDER_URL}/api/tours/test/", timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(f"📧 Email configured: {data.get('email_configured')}")
        print(f"📊 Total bookings: {data.get('total_bookings')}")
        
        # Check if email backend is set
        if not data.get('email_configured'):
            print("\n❌ EMAIL NOT CONFIGURED ON RENDER")
            print("Environment variables missing or incorrect")
    else:
        print(f"❌ Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🔧 RENDER ENVIRONMENT VARIABLES NEEDED:")
print("EMAIL_HOST_USER=anwinws@gmail.com")
print("EMAIL_HOST_PASSWORD=nnpe ocer ziuc wuna") 
print("DEFAULT_FROM_EMAIL=Bellavista Care Homes <noreply@bellavista.com>")
print("EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend")
print("EMAIL_HOST=smtp.gmail.com")
print("EMAIL_PORT=587")
print("EMAIL_USE_TLS=True")

print("\n💡 STEPS TO FIX:")
print("1. Add ALL environment variables above in Render dashboard")
print("2. Redeploy the service")
print("3. Test again")