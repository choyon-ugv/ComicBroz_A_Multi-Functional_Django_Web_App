from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from users.models import User, Movie, Blog, Comic, Profile
from users.forms import ProfileForm
from django.contrib import messages

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
    return render(request, 'admin_index.html', context)



def profile_settings(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        username = request.POST.get('username')
        email = request.POST.get('email')
        if form.is_valid():
            # Update User model
            user = request.user
            user.username = username
            user.email = email
            try:
                user.save()
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile_settings')
            except Exception as e:
                messages.error(request, f'Error updating profile: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'profile_settings.html', {
        'form': form,
        'user': request.user
    })