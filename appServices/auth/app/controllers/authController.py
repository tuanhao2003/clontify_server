from django.views import View
from app.services.authService import AuthService
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from app.serializers.accountSerializer import AccountSerializer
from common.baseResponse import BaseResponse
class GetCsrfToken(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        token = get_token(request)
        return BaseResponse.success(message="Thành công", data={"token": token})

class LoginController(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        
        email = data.get("email", "").strip()
        username = data.get("username", "").strip()
        password = data.get("password", "").strip()
        if not password:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        if (not email and not username) or (email == "" and username == ""):
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        
        result = AuthService.login(username, email, password)
        if result == -1:
            return BaseResponse.notFound("Tài khoản chưa được đăng ký", {"failed": -1})
        if result == -2:
            return BaseResponse.internalError("Xảy ra lỗi trong quá trình đăng nhập", {"failed": -2})
        if result == 0:
            return BaseResponse.unauthorized("Sai tài khoản hoặc mật khẩu", {"failed": 0})
        
        account, token = result
        return BaseResponse.success("Đăng nhập thành công", {
            "access_token": token["access"],
            "refresh_token": token["refresh"],
            "account": AccountSerializer(account).data
        })