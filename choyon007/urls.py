from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import RegisterView, index_view

urlpatterns = [
    path('', RegisterView.as_view(), name='root'),    # Root URL shows register.html
    path('index/', index_view, name='index'),         # Separate index view
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),              # Users app API routes
    path('home/', include('edgecut.urls')),           # Edgecut app routes with prefix
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)