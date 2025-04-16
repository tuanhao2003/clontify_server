from django.views import View
from app.services.authService import AuthService
import json


class LoginController(View):
    def post(self, request):
        data = json.loads(request.body)
        return AuthService.login(data)