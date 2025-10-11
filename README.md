# Bellavista Care Homes - Backend API

## 🚀 Quick Start

### Local Development
```bash
# Automated setup
python deploy.py

# Manual setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🌐 Production Deployment

### Railway (Recommended)
1. Push to GitHub
2. Connect Railway to your repo
3. Set environment variables:
   - `SECRET_KEY`: Generate a secure key
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: your-app.railway.app

### Render
1. Connect GitHub repo
2. Use `build.sh` for build command
3. Use `gunicorn bellavista_backend.wsgi:application` for start command

### Heroku
```bash
git add .
git commit -m "Deploy"
git push heroku main
```

### 2. API Endpoints

- **POST** `/api/tours/book/` - Create tour booking
- **GET** `/api/tours/bookings/` - List all bookings
- **GET** `/api/tours/available-slots/` - Get available time slots
- **GET** `/api/tours/stats/` - Get booking statistics

### 3. Django Concepts for Interviews

#### Models (Database Layer)
```python
# Key concepts: Fields, Relationships, Meta options
class TourBooking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
```

#### Views (Business Logic)
```python
# Function-based views
@api_view(['POST'])
def create_booking(request):
    # Handle request logic
    pass

# Class-based views
class BookingCreateView(generics.CreateAPIView):
    queryset = TourBooking.objects.all()
    serializer_class = BookingSerializer
```

#### Serializers (Data Validation)
```python
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourBooking
        fields = '__all__'
    
    def validate_email(self, value):
        # Custom validation
        return value
```

### 4. Interview Topics to Master

#### Database & ORM
- Models and relationships (ForeignKey, ManyToMany)
- QuerySets and database optimization
- Migrations and schema changes

#### REST API Development
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes and error handling
- Authentication and permissions

#### Django Architecture
- MVT pattern (Model-View-Template)
- URL routing and namespacing
- Middleware and request/response cycle

#### Security
- CSRF protection
- SQL injection prevention
- Authentication and authorization

#### Testing
- Unit tests and integration tests
- Test-driven development (TDD)
- Mock objects and fixtures

### 5. Common Interview Questions

1. **What is Django ORM?**
   - Object-Relational Mapping for database operations
   - Converts Python objects to SQL queries

2. **Explain Django's request-response cycle**
   - URL routing → View → Model → Template → Response

3. **What are Django signals?**
   - Hooks for certain actions (pre_save, post_save)

4. **Difference between select_related and prefetch_related?**
   - select_related: SQL JOIN for ForeignKey
   - prefetch_related: Separate queries for ManyToMany

### 6. Best Practices

- Use virtual environments
- Follow PEP 8 coding standards
- Write comprehensive tests
- Use environment variables for secrets
- Implement proper error handling
- Document your API endpoints