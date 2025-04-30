from django.views import View
from app.services.genresService import GenresService
from app.entities.genres import Genres
from app.serializers.genresSerializer import GenresSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class GenresController(View):
    def get(self, request):
        id = request.GET.get("id")
        name = request.GET.get("name")

        if id:
            result, error = GenresService.findById(id)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy thể loại")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", GenresSerializer(result).data)

        if name:
            result, error = GenresService.findByName(name)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu tên thể loại")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy thể loại")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", GenresSerializer(result, many=True).data)

        return BaseResponse.badRequest("Không có tham số nào hợp lệ")

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        action = data.get("action")
        if action == "create":
            result, error = GenresService.doCreate(
                data.get("name"),
                data.get("description"),
            )
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu trường bắt buộc")
            if error == ErrorCodes.ALREADY_EXISTS:
                return BaseResponse.badRequest("Thể loại đã tồn tại")
            if error == ErrorCodes.CREATE_FAILED:
                return BaseResponse.internalError("Không tạo được thể loại")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Tạo thành công", GenresSerializer(result).data)

        if action == "update":
            result, error = GenresService.doUpdate(Genres(**data))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.UPDATE_FAILED:
                return BaseResponse.internalError("Không cập nhật được thể loại")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Cập nhật thành công", GenresSerializer(result).data)

        if action == "delete":
            result, error = GenresService.doDelete(data.get("id"))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.DELETE_FAILED:
                return BaseResponse.internalError("Không xóa được thể loại")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Xóa thành công")

        return BaseResponse.badRequest("Hành động không hợp lệ") 