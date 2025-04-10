from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Comic, Like, Comment
from django.contrib.auth.decorators import login_required

@login_required(login_url='/api/login/')
def home(request):
    print(f"Home view - User: {request.user}, Authenticated: {request.user.is_authenticated}")
    blogs = Blog.objects.all()[:3]
    comics = Comic.objects.all()[:6]
    return render(request, 'edgecut/index.html', {'blogs': blogs, 'comics': comics})

@login_required(login_url='/api/login/')
def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'edgecut/blog.html', {'blogs': blogs})

@login_required(login_url='/api/login/')
def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comments = Comment.objects.filter(blog=blog).order_by('-created_at')
    recent_blogs = Blog.objects.exclude(id=blog_id)[:5]
    likes_count = Like.objects.filter(blog=blog).count()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(blog=blog, user=request.user).exists()
    
    context = {
        'blog': blog,
        'comments': comments,
        'recent_blogs': recent_blogs,
        'likes_count': likes_count,
        'user_liked': user_liked,
    }
    return render(request, 'edgecut/blog_details.html', context)

@login_required(login_url='/api/login/')
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST' and request.user.is_authenticated:
        like, created = Like.objects.get_or_create(user=request.user, blog=blog)
        if not created:
            like.delete()
    return redirect('blog_detail', blog_id=blog_id)

@login_required(login_url='/api/login/')
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            print(f"Commenting as: {request.user}, Authenticated: {request.user.is_authenticated}")
            Comment.objects.create(
                user=request.user,
                blog=blog,
                content=content
            )
    return redirect('blog_detail', blog_id=blog_id)

@login_required(login_url='/api/login/')
def comic(request):
    comics = Comic.objects.all()
    return render(request, 'edgecut/comics.html', {'comics': comics})

@login_required(login_url='/api/login/')
def about(request):
    return render(request, 'edgecut/about.html')

@login_required(login_url='/api/login/')
def contact(request):
    return render(request, 'edgecut/contact.html')