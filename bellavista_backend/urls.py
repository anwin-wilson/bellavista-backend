"""
URL configuration for bellavista_backend project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tours/', include('tours.urls')),
]
