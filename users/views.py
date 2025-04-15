from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import RegisterForm, LoginForm
from .models import User, Movie, Comic, Blog, Comment, Like

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                # Redirect to 'next' parameter if present, else home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html', {'username': request.user.username})

def movies(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})

def about(request):
    return render(request, 'about.html')

def comic(request):
    comics = Comic.objects.all()
    return render(request, 'comics.html', {'comics': comics})

def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs.html', {'blogs': blogs})

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
    return render(request, 'blog_details.html', context)

def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST' and request.user.is_authenticated:
        like, created = Like.objects.get_or_create(user=request.user, blog=blog)
        if not created:
            like.delete()
    return redirect('blog_detail', blog_id=blog_id)

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

@login_required
def edit_comment(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comment = get_object_or_404(Comment, id=comment_id, blog=blog)
    
    # Check if the user is the comment author
    if comment.user != request.user:
        messages.error(request, "You are not authorized to edit this comment.")
        return redirect('blog_detail', blog_id=blog.id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment.content = content
            comment.save()
            messages.success(request, "Comment updated successfully.")
            return redirect('blog_detail', blog_id=blog.id)
        else:
            messages.error(request, "Comment content cannot be empty.")
    
    return redirect('blog_detail', blog_id=blog.id)

@login_required
def delete_comment(request, blog_id, comment_id):
    blog = get_object_or_404(Blog, id=blog_id)
    comment = get_object_or_404(Comment, id=comment_id, blog=blog)
    
    # Check if the user is the comment author
    if comment.user != request.user:
        messages.error(request, "You are not authorized to delete this comment.")
        return redirect('blog_detail', blog_id=blog.id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('blog_detail', blog_id=blog.id)
    
    return redirect('blog_detail', blog_id=blog.id)

def contact(request):
    return render(request, 'contact.html')

