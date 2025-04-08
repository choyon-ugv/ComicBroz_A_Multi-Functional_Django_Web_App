from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('comics/', views.comic, name='comics'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
