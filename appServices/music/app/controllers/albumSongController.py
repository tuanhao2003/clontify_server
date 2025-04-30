from django.views import View
from app.services.albumSongService import AlbumSongService
from app.entities.albumSong import AlbumSong
from app.serializers.albumSongSerializer import AlbumSongSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class AlbumSongController(View):
    def get(self, request):
        id = request.GET.get("id")
        albumId = request.GET.get("albumId")
        songId = request.GET.get("songId")

        if id:
            result, error = AlbumSongService.findById(id)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy album-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", AlbumSongSerializer(result).data)

        if albumId:
            result, error = AlbumSongService.findByAlbumId(albumId)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu albumId")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy album-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", AlbumSongSerializer(result, many=True).data)

        if songId:
            result, error = AlbumSongService.findBySongId(songId)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu songId")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy album-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", AlbumSongSerializer(result, many=True).data)

        return BaseResponse.badRequest("Không có tham số nào hợp lệ")

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        action = data.get("action")
        if action == "create":
            result, error = AlbumSongService.doCreate(
                data.get("albumId"),
                data.get("songId"),
                data.get("order"),
            )
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu trường bắt buộc")
            if error == ErrorCodes.ALREADY_EXISTS:
                return BaseResponse.badRequest("Album-song đã tồn tại")
            if error == ErrorCodes.CREATE_FAILED:
                return BaseResponse.internalError("Không tạo được album-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Tạo thành công", AlbumSongSerializer(result).data)

        if action == "update":
            result, error = AlbumSongService.doUpdate(AlbumSong(**data))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.UPDATE_FAILED:
                return BaseResponse.internalError("Không cập nhật được album-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Cập nhật thành công", AlbumSongSerializer(result).data)

        if action == "delete":
            result, error = AlbumSongService.doDelete(data.get("id"))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.DELETE_FAILED:
                return BaseResponse.internalError("Không xóa được album-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Xóa thành công")

        return BaseResponse.badRequest("Hành động không hợp lệ") 