from django.views import View
from app.services.accountsService import AccountsService
from app.serializers.accountSerializer import AccountSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json
from datetime import datetime
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import AccessToken


class GetAccount(View):
    def get(self, request):
        id = request.GET.get("id")
        username = request.GET.get("username")
        email = request.GET.get("email")
        status = request.GET.get("status")
        start = request.GET.get("start")
        end = request.GET.get("end")

        if id:
            result, error = AccountsService.findById(id)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy tài khoản")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", AccountSerializer(result).data)

        if username:
            result, error = AccountsService.findByUsername(username)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu username")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy tài khoản")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", AccountSerializer(result).data)

        if email:
            result, error = AccountsService.findByEmail(email)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu email")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy tài khoản")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", AccountSerializer(result).data)

        if status is not None:
            result, error = AccountsService.findByStatus(status.lower() == "true")
            if error == ErrorCodes.INVALID_STATUS:
                return BaseResponse.badRequest("Thiếu trạng thái")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy tài khoản nào")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success(
                "Thành công", AccountSerializer(result, many=True).data
            )

        if start and end:
            result, error = AccountsService.findByDateCreated(start, end)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Ngày không hợp lệ")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy tài khoản nào")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success(
                "Thành công", AccountSerializer(result, many=True).data
            )

        return BaseResponse.badRequest("Không có tham số nào hợp lệ")


class DeleteAccount(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        id = data.get("id")
        result, error = AccountsService.doDelete(id)
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("Thiếu ID")
        if error == ErrorCodes.DELETE_FAILED:
            return BaseResponse.internalError("Không xoá được tài khoản")
        if error:
            return BaseResponse.internalError("Lỗi hệ thống")
        return BaseResponse.success("Xoá thành công")


class UpdateAccount(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        authHeader = request.headers.get("Authorization")
        accountID = None
        if authHeader and authHeader.startswith("Bearer "):
            tokenStr = authHeader.split(" ")[1]
            try:
                token = AccessToken(tokenStr)
                accountID = token.get("user_id")
            except (TokenError, InvalidToken):
                return BaseResponse.invalidToken("Token không hợp lệ")

        currentAccount, error = AccountsService.findById(accountID)
        if error:
            return BaseResponse.notFound("Không tìm thấy tài khoản")

        if data.get('password'):
            currentAccount.password = data.get('password')
        if data.get('email'):
            currentAccount.email = data.get('email')
        if data.get('roleId'):
            currentAccount.roleId = data.get('roleId')

        result, error = AccountsService.doUpdate(currentAccount)
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("Thiếu ID")
        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Không tìm thấy tài khoản")
        if error == ErrorCodes.ALREADY_EXISTS:
            return BaseResponse.badRequest("Email đã tồn tại")
        if error == ErrorCodes.UPDATE_FAILED:
            return BaseResponse.internalError("Không cập nhật được tài khoản")
        if error:
            return BaseResponse.internalError("Lỗi hệ thống")
        return BaseResponse.success(
            "Cập nhật thành công", AccountSerializer(result).data
        )