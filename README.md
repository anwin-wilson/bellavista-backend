# Bellavista Care Homes - Backend API

A Django REST API for managing tour bookings at Bellavista Care Homes.

## 🚀 Quick Start

### Local Development
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🌐 Render Deployment

### Build Command
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

### Start Command
```bash
gunicorn bellavista_backend.wsgi:application
```

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com,localhost,127.0.0.1
SENDGRID_API_KEY=your-sendgrid-key  # Optional for email
```

## 📡 API Endpoints

- **POST** `/api/tours/book/` - Create tour booking
- **GET** `/api/tours/bookings/` - List all bookings
- **GET** `/api/tours/available-slots/` - Get available time slots
- **GET** `/api/tours/stats/` - Get booking statistics
- **GET** `/api/tours/test/` - Health check endpoint

## 🏗️ Project Structure

```
bellavista_backend/
├── bellavista_backend/     # Django project settings
├── tours/                  # Main app
│   ├── models.py          # Database models
│   ├── views.py           # API endpoints
│   ├── serializers.py     # Data validation
│   └── email_service.py   # Email functionality
├── requirements.txt       # Dependencies
└── manage.py             # Django management
```

## 🔧 Features

- **Tour Booking Management**: Create and manage tour bookings
- **Available Slots**: Check time slot availability
- **Email Notifications**: SendGrid integration (optional)
- **Admin Interface**: Django admin for booking management
- **Statistics**: Booking analytics and reporting

## 📊 Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Email**: SendGrid API
- **Deployment**: Render
- **Static Files**: WhiteNoise

## 🛠️ Development

### Running Tests
```bash
python manage.py test
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

### Collecting Static Files
```bash
python manage.py collectstatic
```

## 📝 License

This project is proprietary software for Bellavista Care Homes.