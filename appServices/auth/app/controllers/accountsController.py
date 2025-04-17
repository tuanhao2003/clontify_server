from django.views import View
from app.services.authService import AuthService
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.http import JsonResponse

