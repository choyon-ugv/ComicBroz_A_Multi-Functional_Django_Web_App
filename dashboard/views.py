from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import User, Movie, Blog, Comic, Profile
from users.forms import ProfileForm, PasswordChangeForm
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy


def admin_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None and (user.is_staff or user.is_superuser):
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not authorized.")

    return render(request, 'custom_admin/admin_login.html', )


@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
def admin_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'admin_change_password.html', {'form': form})

@login_required(login_url='admin_login')
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
    return render(request, 'custom_admin/admin_index.html', context)


@login_required
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

@login_required
def profile_list(request):
    profiles = Profile.objects.filter(user__is_superuser = False, user__is_staff = False)
    context = {
        'profiles' : profiles
    }
    return render(request, 'profile_list.html', context)


def profile_datatable_view(request):
    # Get DataTables parameters
    draw = int(request.POST.get('draw', 1))
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    search_value = request.POST.get('search[value]', '')
    order_column = int(request.POST.get('order[0][column]', 0))
    order_dir = request.POST.get('order[0][dir]', 'asc')

    # Map column index to field
    columns = ['id', 'user__username', 'user__email', 'bio', 'level', 'progress']
    order_field = columns[order_column]
    if order_dir == 'desc':
        order_field = f'-{order_field}'

    # Build queryset
    queryset = Profile.objects.select_related('user').all()
    if search_value:
        queryset = queryset.filter(
            Q(user__username__icontains=search_value) |
            Q(user__email__icontains=search_value) |
            Q(bio__icontains=search_value)
        )

    # Apply ordering
    queryset = queryset.order_by(order_field)

    # Paginate
    paginator = Paginator(queryset, length)
    page_number = (start // length) + 1
    page_obj = paginator.get_page(page_number)

    # Prepare data
    data = []
    for index, profile in enumerate(page_obj, start=start + 1):
        view_url = reverse('profile_view', args=[profile.pk])
        edit_url = reverse('profile_edit', args=[profile.pk])
        data.append({
            'id': index,
            'username': profile.user.username,
            'email': profile.user.email,
            'bio': profile.bio or 'N/A',
            'level': profile.level,
            'progress': f"{profile.progress}%",
            'action': (
                f'<a href="{view_url}" class="btn btn-sm btn-info">View</a> '
                f'<a href="{edit_url}" class="btn btn-sm btn-warning">Edit</a>'
            )
        })

    # Response
    return JsonResponse({
        'draw': draw,
        'recordsTotal': Profile.objects.count(),
        'recordsFiltered': paginator.count,
        'data': data
    })


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile_view.html'

class ProfileEditView(UpdateView):
    model = Profile
    fields = ['bio', 'level', 'progress', 'profile_image']
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('myapp:profile_list')