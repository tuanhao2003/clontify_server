from django.views import View
from app.services.authService import AuthService
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from app.serializers.accountSerializer import AccountSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes

# log
import logging
log = logging.getLogger(__name__)

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

        if not password or (not email and not username):
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        result, error = AuthService.login(username=username, email=email, password=password)

        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Tài khoản chưa được đăng ký")
        if error == ErrorCodes.UNAUTHORIZED:
            return BaseResponse.unauthorized("Sai tài khoản hoặc mật khẩu")
        if error == ErrorCodes.OPERATION_FAILED:
            return BaseResponse.internalError("Xảy ra lỗi trong quá trình đăng nhập")
        if error:
            log.error(f"Hệ thống lỗi: {str(error)}")
            return BaseResponse.internalError("Lỗi hệ thống")

        return BaseResponse.success("Đăng nhập thành công", {
            "access_token": result["tokens"]["access"],
            "refresh_token": result["tokens"]["refresh"],
            "account": AccountSerializer(result["account"]).data
        })
    
class RegisterController(View):
    def post(self, request):
        import logging
        logger = logging.getLogger(__name__)
        logger.info("[Register] Nhận yêu cầu đăng ký mới")
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.warning("[Register] JSON không hợp lệ")
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        username = data.get("username", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "").strip()
        fullName = data.get("fullName", "noname").strip()
        avatarUrl = data.get("avatarUrl")
        bio = data.get("bio")
        dateOfBirth = data.get("dateOfBirth")
        phoneNumber = data.get("phoneNumber")

        if not username or not email or not password:
            logger.warning("[Register] Thiếu thông tin cần thiết - username/email/password")
            return BaseResponse.badRequest("Thiếu thông tin đăng ký")

        logger.info(f"[Register] Đang xử lý đăng ký cho username: {username}, email: {email}")

        result, error = AuthService.register(
            username=username,
            password=password,
            email=email,
            fullName=fullName,
            avatarUrl=avatarUrl,
            bio=bio,
            dateOfBirth=dateOfBirth,
            phoneNumber=phoneNumber
        )

        if error == ErrorCodes.ALREADY_EXISTS:
            logger.warning(f"[Register] Tài khoản đã tồn tại - username: {username}, email: {email}")
            return BaseResponse.badRequest("Email hoặc tên người dùng đã tồn tại")
        if error == ErrorCodes.CREATE_FAILED:
            logger.error(f"[Register] Lỗi khi tạo tài khoản - username: {username}")
            return BaseResponse.internalError("Xảy ra lỗi khi tạo tài khoản")
        if error == ErrorCodes.OPERATION_FAILED:
            logger.error(f"[Register] Lỗi trong quá trình đăng ký - username: {username}")
            return BaseResponse.internalError("Xảy ra lỗi trong quá trình đăng ký")
        if error:
            logger.critical(f"[Register] Lỗi hệ thống không xác định - username: {username}")
            return BaseResponse.internalError("Lỗi hệ thống")

        logger.info(f"[Register] Tạo tài khoản thành công - username: {username}")
        return BaseResponse.success("Tạo tài khoản thành công", {
            "account": AccountSerializer(result["account"]).data,
            "profile": result["profile"],
        })

class RefreshToken(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        refreshToken = data.get("refreshToken")
        if not refreshToken:
            return BaseResponse.badRequest("Thiếu refresh token")

        tokens, error = AuthService.refreshToken(refreshToken)
        
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.unauthorized("Token không hợp lệ")
        if error == ErrorCodes.OPERATION_FAILED:
            return BaseResponse.internalError("Xảy ra lỗi khi làm mới token")
        if error:
            return BaseResponse.internalError("Lỗi hệ thống")

        return BaseResponse.success("Làm mới token thành công", {
            "accessToken": tokens["access"],
            "refreshToken": tokens["refresh"]
        })