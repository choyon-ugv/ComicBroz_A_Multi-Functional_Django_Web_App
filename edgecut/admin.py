from django.contrib import admin
from .models import Blog, Comic, Like, Comment

admin.site.register(Blog)
admin.site.register(Comic)
admin.site.register(Like)
admin.site.register(Comment)