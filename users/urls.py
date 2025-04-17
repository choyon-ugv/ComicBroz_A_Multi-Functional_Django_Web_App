from django.urls import path
from .views import register, login, logout, home, movies, about, comic, blog, contact, like_blog, add_comment, blog_detail, edit_comment, delete_comment, change_password, profile_view, profile_update, comic_detail_view #movie_detail

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('password_change/', change_password, name='change_password'),
    path('logout/', logout, name='logout'),
    path('', home, name='home'),
    path('movies/', movies, name='movies'),
    # path('movies/<int:pk>/', movie_detail, name='movie_detail'),
    path('about/', about, name='about'),
    path('comics/', comic, name='comics'),
    path('comics/<int:pk>/', comic_detail_view, name='comic_detail'),
    path('contact/', contact, name='contact'),
    path('blogs/', blog, name='blogs'),
    path('blogs/<int:blog_id>/', blog_detail, name='blog_detail'),
    path('blogs/<int:blog_id>/like/', like_blog, name='like_blog'),
    path('blogs/<int:blog_id>/comment/', add_comment, name='add_comment'),
    path('blogs/<int:blog_id>/edit_comment/<int:comment_id>/', edit_comment, name='edit_comment'),
    path('blogs/<int:blog_id>/delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', profile_update, name='profile-update'),
]