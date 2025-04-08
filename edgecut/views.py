from django.shortcuts import render
from .models import Blog, Comic
def home(request):
    blogs = Blog.objects.all()[:3]  # Get the first 3 blog posts
    comics = Comic.objects.all()[:6]  # Get the first 3 comics
    return render(request, 'edgecut/index.html', {'blogs': blogs, 'comics': comics})

def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'edgecut/blog.html', {'blogs': blogs})

def comic(request):
    comics = Comic.objects.all()
    return render(request, 'edgecut/comics.html', {'comics': comics})

def about(request):
    return render(request, 'edgecut/about.html')

def contact(request):
    return render(request, 'edgecut/contact.html')


