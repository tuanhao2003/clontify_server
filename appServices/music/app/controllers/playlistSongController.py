from django.views import View
from app.services.playlistSongService import PlaylistSongService
from app.entities.playlistSong import PlaylistSong
from app.serializers.playlistSongSerializer import PlaylistSongSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class PlaylistSongController(View):
    def get(self, request):
        id = request.GET.get("id")
        playlistId = request.GET.get("playlistId")
        songId = request.GET.get("songId")

        if id:
            result, error = PlaylistSongService.findById(id)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy playlist-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", PlaylistSongSerializer(result).data)

        if playlistId:
            result, error = PlaylistSongService.findByPlaylistId(playlistId)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu playlistId")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy playlist-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", PlaylistSongSerializer(result, many=True).data)

        if songId:
            result, error = PlaylistSongService.findBySongId(songId)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu songId")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy playlist-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Thành công", PlaylistSongSerializer(result, many=True).data)

        return BaseResponse.badRequest("Không có tham số nào hợp lệ")

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        action = data.get("action")
        if action == "create":
            result, error = PlaylistSongService.doCreate(
                data.get("playlistId"),
                data.get("songId"),
                data.get("order"),
            )
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu trường bắt buộc")
            if error == ErrorCodes.ALREADY_EXISTS:
                return BaseResponse.badRequest("Playlist-song đã tồn tại")
            if error == ErrorCodes.CREATE_FAILED:
                return BaseResponse.internalError("Không tạo được playlist-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Tạo thành công", PlaylistSongSerializer(result).data)

        if action == "update":
            result, error = PlaylistSongService.doUpdate(PlaylistSong(**data))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.UPDATE_FAILED:
                return BaseResponse.internalError("Không cập nhật được playlist-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Cập nhật thành công", PlaylistSongSerializer(result).data)

        if action == "delete":
            result, error = PlaylistSongService.doDelete(data.get("id"))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.DELETE_FAILED:
                return BaseResponse.internalError("Không xóa được playlist-song")
            if error:
                return BaseResponse.internalError("Lỗi hệ thống")
            return BaseResponse.success("Xóa thành công")

        return BaseResponse.badRequest("Hành động không hợp lệ") 