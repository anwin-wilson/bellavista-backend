"""
URL configuration for bellavista_backend project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tours/', include('tours.urls')),
    # SPA fallback - serve index.html for all non-API routes
    re_path(r'^(?!api/).*$', TemplateView.as_view(template_name='index.html'), name='spa-fallback'),
]
