#!/usr/bin/env python
"""
Keep Render service alive by pinging it every 10 minutes
Run this on your local machine or a free service
"""

import requests
import time
import schedule
from datetime import datetime

RENDER_URL = "https://bellavista-backend-3.onrender.com"

def ping_service():
    try:
        response = requests.get(f"{RENDER_URL}/api/tours/stats/", timeout=30)
        print(f"✅ {datetime.now().strftime('%H:%M:%S')} - Pinged successfully ({response.status_code})")
    except Exception as e:
        print(f"❌ {datetime.now().strftime('%H:%M:%S')} - Ping failed: {e}")

# Schedule ping every 10 minutes
schedule.every(10).minutes.do(ping_service)

print("🔄 Starting keep-alive service...")
print("Press Ctrl+C to stop")

# Initial ping
ping_service()

# Keep running
while True:
    schedule.run_pending()
    time.sleep(60)