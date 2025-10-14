# Main URL Configuration for Bellavista Care Homes Backend

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Interface
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/tours/', include('tours.urls')),
]
