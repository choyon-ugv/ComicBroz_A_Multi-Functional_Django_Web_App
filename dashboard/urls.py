from django.urls import path
from .views import admin_dashboard, profile_settings

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('profile_settings/', profile_settings, name='profile_settings')
]