from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):  
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    
class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    runtime =models.PositiveIntegerField(help_text="Runtime in minutes")
    image = models.ImageField(upload_to='movies/images/', blank=True, null=True)
    description = models.TextField()
    watch_link = models.URLField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.title

    
class Comic(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='comic_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title
    
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')
        
    def __str__(self):
        return f"{self.user.username} liked {self.blog.title}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title}"
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank=True)
    profile_image = models.ImageField(upload_to='profile_pics/', default='default.png')
    favorite_quote = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"