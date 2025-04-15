from django.urls import path
from .views import register, login, logout, home, movies, about, comic, blog, contact, like_blog, add_comment, blog_detail, edit_comment, delete_comment

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('', home, name='home'),
    path('movies/', movies, name='movies'),
    path('about/', about, name='about'),
    path('comics/', comic, name='comics'),
    path('contact/', contact, name='contact'),
    path('blogs/', blog, name='blogs'),
    path('blogs/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('blogs/<int:blog_id>/like/', like_blog, name='like_blog'),
    path('blogs/<int:blog_id>/comment/', add_comment, name='add_comment'),
    path('blogs/<int:blog_id>/edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('blogs/<int:blog_id>/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
]