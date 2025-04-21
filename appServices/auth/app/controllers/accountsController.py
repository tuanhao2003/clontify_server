from django.views import View
from app.services.accountsService import AccountsService
from app.serializers.accountSerializer import AccountSerializer
from common.baseResponse import BaseResponse
import json
from datetime import datetime


class GetAccount(View):
    def get(self, request):
        id = request.GET.get("id")
        username = request.GET.get("username")
        email = request.GET.get("email")
        status = request.GET.get("status")
        start = request.GET.get("start")
        end = request.GET.get("end")

        if id:
            result = AccountsService.findByID(id)
            if result == -1:
                return BaseResponse.badRequest("Thiếu ID")
            if not result:
                return BaseResponse.notFound("Không tìm thấy tài khoản")
            return BaseResponse.success("Thành công", AccountSerializer(result).data)

        if username:
            result = AccountsService.findByUsername(username)
            if result == -1:
                return BaseResponse.badRequest("Thiếu username")
            if not result:
                return BaseResponse.notFound("Không tìm thấy tài khoản")
            return BaseResponse.success("Thành công", AccountSerializer(result).data)

        if email:
            result = AccountsService.findByEmail(email)
            if result == -1:
                return BaseResponse.badRequest("Thiếu email")
            if not result:
                return BaseResponse.notFound("Không tìm thấy tài khoản")
            return BaseResponse.success("Thành công", AccountSerializer(result).data)

        if status is not None:
            result = AccountsService.findByStatus(status.lower() == "true")
            if result == -1:
                return BaseResponse.badRequest("Thiếu trạng thái")
            if not result:
                return BaseResponse.notFound("Không tìm thấy tài khoản nào")
            return BaseResponse.success(
                "Thành công", AccountSerializer(result, many=True).data
            )

        if start and end:
            result = AccountsService.findByDateCreated(start, end)
            if result == -1:
                return BaseResponse.badRequest("Ngày không hợp lệ")
            if not result:
                return BaseResponse.notFound("Không tìm thấy tài khoản nào")
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
        result = AccountsService.doDelete(id)
        if result == -1:
            return BaseResponse.badRequest("Thiếu ID")
        if result is None:
            return BaseResponse.success("Xoá thành công")
        return BaseResponse.internalError("Không xoá được tài khoản")


class UpdateAccount(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        result = AccountsService.doUpdate(AccountSerializer.deserialize(data))
        if result == -1:
            return BaseResponse.badRequest("Thiếu ID")
        if result is None:
            return BaseResponse.notFound("Không tìm thấy hoặc email đã tồn tại")
        return BaseResponse.success(
            "Cập nhật thành công", AccountSerializer(result).data
        )
