from django.urls import path
from .views import admin_login, admin_logout, admin_change_password, admin_dashboard, profile_settings, profile_list, profile_datatable_view, ProfileView, ProfileEditView, ProfileDeleteView, blog_list, comic_list

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_logout/', admin_logout, name='admin_logout'),
    path('admin_change_password/', admin_change_password, name='admin_change_password'),
    path('profile_settings/', profile_settings, name='profile_settings'),
    path('profile_list/', profile_list,  name='profile_list'),
    path('ajax_datatable/profiles/', profile_datatable_view, name='profile_datatable'),
    path('profile/<int:pk>/view/', ProfileView.as_view(), name='profile_view'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile_delete' ),
    path('blog_list/', blog_list, name='blog_list'),
    path('comic_list/',comic_list, name='comic_list',)
]