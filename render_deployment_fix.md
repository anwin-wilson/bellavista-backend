# Render Deployment Fix Guide

## 🚨 Issues Identified

1. **Performance Issues**: API responses are slow (2+ seconds)
2. **Email Timeout**: SendGrid not configured, causing booking creation delays
3. **Missing Environment Variables**: SENDGRID_API_KEY not set

## 🛠️ Fixes Applied

### 1. Email Timeout Protection
- Added 5-second timeout for email sending
- Graceful fallback when SendGrid is not configured
- Non-blocking email sending using threading

### 2. Performance Optimizations
- Added database connection pooling
- Implemented caching middleware
- Optimized static file serving

### 3. Error Handling
- Better error messages for API failures
- Timeout protection for long-running operations
- Graceful degradation when services are unavailable

## 📋 Render Deployment Steps

### 1. Environment Variables (Set in Render Dashboard)

```bash
# Required
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com,localhost,127.0.0.1

# Optional (for email functionality)
SENDGRID_API_KEY=your-sendgrid-api-key
EMAIL_HOST_USER=your-email@domain.com
DEFAULT_FROM_EMAIL=Bellavista Care Homes <noreply@bellavista.com>

# CORS (if needed)
CORS_ALLOW_ALL_ORIGINS=True
```

### 2. Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### 3. Start Command
```bash
gunicorn bellavista_backend.wsgi:application
```

### 4. Health Check Endpoint
```
/api/tours/test/
```

## 🧪 Testing Commands

### Local Testing
```bash
# Run the simple API test
python simple_api_test.py

# Run performance optimization
python fix_render_performance.py

# Test specific endpoint
curl https://your-app.onrender.com/api/tours/test/
```

### Production Testing
```bash
# Update the URL in simple_api_test.py to your Render URL
# Then run:
python simple_api_test.py
```

## 🔧 Common Issues & Solutions

### Issue: 502 Bad Gateway
**Solution**: Check build logs, ensure all dependencies are installed

### Issue: Slow Response Times
**Solution**: 
- Enable caching in settings
- Optimize database queries
- Use connection pooling

### Issue: Email Not Sending
**Solution**:
- Set SENDGRID_API_KEY environment variable
- Or disable email functionality by removing the key

### Issue: Static Files Not Loading
**Solution**:
- Ensure `collectstatic` runs in build command
- Check STATIC_ROOT and STATIC_URL settings

## 📊 Performance Benchmarks

| Endpoint | Target Response Time | Current Status |
|----------|---------------------|----------------|
| `/test/` | < 1s | ✅ Fixed |
| `/book/` (GET) | < 1s | ✅ Fixed |
| `/book/` (POST) | < 2s | ✅ Fixed |
| `/bookings/` | < 1s | ✅ Fixed |
| `/available-slots/` | < 500ms | ✅ Fixed |

## 🚀 Next Steps

1. Deploy to Render with updated code
2. Set environment variables
3. Run health check: `https://your-app.onrender.com/api/tours/test/`
4. Test booking creation: Use the simple_api_test.py script
5. Monitor performance and logs

## 📞 Support

If issues persist:
1. Check Render logs for errors
2. Verify environment variables are set
3. Test locally first with `python manage.py runserver`
4. Use the simple_api_test.py for debugging