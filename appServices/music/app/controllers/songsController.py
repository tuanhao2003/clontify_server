from django.views import View
from app.services.songsService import SongsService
from app.entities.songs import Songs
from app.serializers.songsSerializer import SongsSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class SongsController(View):
    def get(self, request):
        id = request.GET.get("id")
        title = request.GET.get("title")
        artistId = request.GET.get("artistId")
        genreId = request.GET.get("genreId")

        if id:
            result, error = SongsService.findById(id)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy bài hát")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", SongsSerializer(result).data)

        if title:
            result, error = SongsService.findByTitle(title)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu tiêu đề")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy bài hát")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)

        if artistId:
            result, error = SongsService.findByArtistId(artistId)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu artistId")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy bài hát")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)

        if genreId:
            result, error = SongsService.findByGenreId(genreId)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu genreId")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy bài hát")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)

        return BaseResponse.badRequest("Không có tham số nào hợp lệ")

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        action = data.get("action")
        if action == "create":
            result, error = SongsService.doCreate(
                data.get("title"),
                data.get("description"),
                data.get("artistId"),
                data.get("genreId"),
                data.get("audioUrl"),
                data.get("backgroundImage"),
                data.get("duration"),
            )
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu trường bắt buộc")
            if error == ErrorCodes.ALREADY_EXISTS:
                return BaseResponse.badRequest("Bài hát đã tồn tại")
            if error == ErrorCodes.CREATE_FAILED:
                return BaseResponse.internalError("Không tạo được bài hát")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Tạo thành công", SongsSerializer(result).data)

        if action == "update":
            result, error = SongsService.doUpdate(Songs(**data))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.UPDATE_FAILED:
                return BaseResponse.internalError("Không cập nhật được bài hát")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Cập nhật thành công", SongsSerializer(result).data)

        if action == "delete":
            result, error = SongsService.doDelete(data.get("id"))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.DELETE_FAILED:
                return BaseResponse.internalError("Không xóa được bài hát")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Xóa thành công")

        return BaseResponse.badRequest("Hành động không hợp lệ") 