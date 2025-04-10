from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser

class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization', '')
        print(f"Request Path: {request.path}, Auth Header: {auth_header}")
        if auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1]
            try:
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                print(f"Validated User: {user}")
                request.user = user
            except Exception as e:
                print(f"Token Validation Error: {e}")
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()