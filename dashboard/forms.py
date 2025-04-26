from django import forms
from users.models import Blog, Comic

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'image', 'content']

class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = ['title', 'description', 'price', 'image']