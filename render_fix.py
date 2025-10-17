import requests
import time

def wake_render():
    """Force wake Render service with multiple attempts"""
    url = "https://bellavista-backend-3.onrender.com"
    
    print("🔄 Attempting to wake Render service...")
    
    for attempt in range(3):
        try:
            print(f"Attempt {attempt + 1}/3...")
            response = requests.get(f"{url}/api/tours/stats/", timeout=60)
            print(f"✅ Service awake! Status: {response.status_code}")
            return True
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                print("Waiting 30 seconds...")
                time.sleep(30)
    
    print("❌ Failed to wake service after 3 attempts")
    return False

if __name__ == "__main__":
    wake_render()