from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserRegistrationSerializer, ChangePasswordSerializer
from .models import User, Movie
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.decorators import login_required

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response = {
                'status': 201,
                'success': True,
                'message': 'User registered successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        return render(request, 'auth/login.html')
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        print(f"Login - Email: {email}, User: {user}")
        if user is not None:
            refresh = RefreshToken.for_user(user)
            print(f"Token for: {user.email}, ID: {user.id}")
            return Response({
                'status': 200,
                'success': True,
                'message': 'User logged in successfully',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'redirect': '/home/',  # Redirect to home page
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 400,
            'success': False,
            'message': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Successfully logged out'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except InvalidToken:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except TokenError as e:
            return Response(
                {'error': f'Token error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Logout failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Old password is not correct'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            response = {
                'status': 200,
                'success': True,
                'message': 'Password updated successfully',
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
def index_view(request):
    return render(request, 'auth/index.html')

@login_required(login_url='/login/')
def movie_blog(request):
    movies = Movie.objects.all()
    return render(request, 'auth/movie_blog.html', {'movies': movies})