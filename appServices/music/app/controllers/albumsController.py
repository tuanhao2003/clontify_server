from django.views import View
from app.services.albumsService import AlbumsService
from app.entities.albums import Albums
from app.serializers.albumsSerializer import AlbumsSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class AlbumsController(View):
    def get(self, request):
        id = request.GET.get("id")
        name = request.GET.get("name")

        if id:
            result, error = AlbumsService.findById(id)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy album")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", AlbumsSerializer(result).data)

        if name:
            result, error = AlbumsService.findByName(name)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu tên album")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy album")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", AlbumsSerializer(result, many=True).data)

        return BaseResponse.badRequest("Không có tham số nào hợp lệ")

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        action = data.get("action")
        if action == "create":
            result, error = AlbumsService.doCreate(
                data.get("name"),
                data.get("description"),
                data.get("backgroundImage"),
            )
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu trường bắt buộc")
            if error == ErrorCodes.ALREADY_EXISTS:
                return BaseResponse.badRequest("Album đã tồn tại")
            if error == ErrorCodes.CREATE_FAILED:
                return BaseResponse.internalError("Không tạo được album")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Tạo thành công", AlbumsSerializer(result).data)

        if action == "update":
            result, error = AlbumsService.doUpdate(Albums(**data))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.UPDATE_FAILED:
                return BaseResponse.internalError("Không cập nhật được album")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Cập nhật thành công", AlbumsSerializer(result).data)

        if action == "delete":
            result, error = AlbumsService.doDelete(data.get("id"))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.DELETE_FAILED:
                return BaseResponse.internalError("Không xóa được album")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Xóa thành công")

        return BaseResponse.badRequest("Hành động không hợp lệ") 