@echo off
echo Testing POST functionality on Railway deployment
echo ================================================

set RAILWAY_URL=https://bellavista-backend-production.up.railway.app

echo.
echo 1. Testing connection...
curl -s -o nul -w "Status: %%{http_code}\n" %RAILWAY_URL%/api/tours/test/

echo.
echo 2. Testing GET on booking endpoint...
curl -s %RAILWAY_URL%/api/tours/book/

echo.
echo 3. Testing POST booking creation...
curl -X POST %RAILWAY_URL%/api/tours/book/ ^
  -H "Content-Type: application/json" ^
  -d "{\"first_name\":\"Test\",\"last_name\":\"User\",\"email\":\"test@example.com\",\"phone_number\":\"+44 7700 900123\",\"preferred_home\":\"cardiff\",\"preferred_date\":\"2025-01-20\",\"preferred_time\":\"14:00\",\"notes\":\"Test booking from curl\"}"

echo.
echo 4. Testing available slots...
curl -s "%RAILWAY_URL%/api/tours/available-slots/?date=2025-01-20&home=cardiff"

echo.
echo 5. Testing booking stats...
curl -s %RAILWAY_URL%/api/tours/stats/

echo.
echo ================================================
echo Test completed!
pause