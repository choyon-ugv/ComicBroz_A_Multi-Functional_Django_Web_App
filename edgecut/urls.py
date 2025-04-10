from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/like/', views.like_blog, name='like_blog'),
    path('blog/<int:blog_id>/comment/', views.add_comment, name='add_comment'),
    path('comics/', views.comic, name='comics'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]