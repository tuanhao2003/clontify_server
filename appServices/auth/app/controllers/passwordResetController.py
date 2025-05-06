from django.views import View
from app.services.passwordResetService import PasswordResetService
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class RequestPasswordReset(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        email = data.get("email")
        if not email:
            return BaseResponse.badRequest("Thiếu email")

        result, error = PasswordResetService.requestPasswordReset(email)
        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Không tìm thấy tài khoản với email này")
        if error == ErrorCodes.OPERATION_FAILED:
            return BaseResponse.internalError("Không thể gửi email")
        if error:
            return BaseResponse.internalError("Lỗi hệ thống")

        return BaseResponse.success("Đã gửi mã xác thực qua email", result)

class VerifyAndResetPassword(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        token = data.get("token")
        verification_code = data.get("verification_code")
        new_password = data.get("new_password")

        if not token or not verification_code or not new_password:
            return BaseResponse.badRequest("Thiếu thông tin cần thiết")

        result, error = PasswordResetService.verifyAndResetPassword(
            token, verification_code, new_password
        )
        if error == ErrorCodes.TOKEN_EXPIRED:
            return BaseResponse.badRequest("Mã xác thực đã hết hạn")
        if error == ErrorCodes.INVALID_VERIFICATION_CODE:
            return BaseResponse.badRequest("Mã xác thực không đúng")
        if error == ErrorCodes.INVALID_TOKEN:
            return BaseResponse.badRequest("Token không hợp lệ")
        if error:
            return BaseResponse.internalError("Lỗi hệ thống")

        return BaseResponse.success("Đặt lại mật khẩu thành công") 