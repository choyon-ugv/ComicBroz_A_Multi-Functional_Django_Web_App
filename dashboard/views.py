from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from users.models import User, Movie, Blog, Comic, Profile
from users.forms import ProfileForm

def admin_dashboard(request):
    total_users = User.objects.count()
    total_movies = Movie.objects.count()
    total_blog = Blog.objects.count()
    total_comic = Comic.objects.count()
    
    context ={
        'total_users': total_users,
        'total_movies': total_movies,
        'total_blog': total_blog,
        'total_comic': total_comic, 
    }
    return render(request, 'index.html', context)

def profile_settings(request):
    return render(request, 'profile_settings.html')


def account_settings_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Success')  # or show success message
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_settings.html', {
        'form': form,
        'profile': profile
    })