from django.views import View
from app.services.albumSongService import AlbumSongService
from app.serializers.albumSongSerializer import AlbumSongSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json


class GetAlbumSong(View):

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            albumId = data.get("albumID")
            songId = data.get("songID")
            page = int(data.get("page", "1"))
            pageSize = int(data.get("pageSize", "10"))

            if albumId and songId:
                result, error = AlbumSongService.findExactly(
                    albumId=albumId, songId=songId
                )
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Không tìm thấy")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success(
                    "Thành công", AlbumSongSerializer(result).data
                )

            if albumId and albumId != "":
                result, error = AlbumSongService.findByAlbumIdPaginated(
                    albumId, page, pageSize
                )
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Không tìm thấy")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success(
                    "Thành công",
                    {
                        "result": AlbumSongSerializer(result["result"], many=True).data,
                        "total": result["total"],
                        "totalPages": result["totalPages"],
                        "currentPage": result["currentPage"],
                    },
                )

            if songId and songId != "":
                result, error = AlbumSongService.findBySongIdPaginated(
                    songId, page, pageSize
                )
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Không tìm thấy")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success(
                    "Thành công",
                    {
                        "result": AlbumSongSerializer(result["result"], many=True).data,
                        "total": result["total"],
                        "totalPages": result["totalPages"],
                        "currentPage": result["currentPage"],
                    },
                )

            result, error = AlbumSongService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Không tìm thấy album")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success(
                "Thành công",
                {
                    "result": AlbumSongSerializer(result["result"], many=True).data,
                    "total": result["total"],
                    "totalPages": result["totalPages"],
                    "currentPage": result["currentPage"],
                },
            )

        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))


class CreateAlbumSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            albumId = data.get("albumID")
            songId = data.get("songID")
            songIds = data.get("songIDs")

            if not albumId or (not songId and not songIds) or albumId == "" or (songId == "" and len(songIds) == 0):
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            if songId:
                result, error = AlbumSongService.doCreate(albumId=albumId, songId=songId)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.ALREADY_EXISTS:
                        return BaseResponse.badRequest("Đã tồn tại")
                    elif error == ErrorCodes.CREATE_FAILED:
                        return BaseResponse.internalError("Tạo thất bại")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))

                return BaseResponse.success("Thành công", AlbumSongSerializer(result).data)
            else:
                result, error = AlbumSongService.doAddSongsToAlbum(albumId=albumId, songIds=songIds)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.ALREADY_EXISTS:
                        return BaseResponse.badRequest("Đã tồn tại")
                    elif error == ErrorCodes.CREATE_FAILED:
                        return BaseResponse.internalError("Tạo thất bại")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))

                return BaseResponse.success("Thành công", AlbumSongSerializer(result, many=True).data)
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))


class DeleteAlbumSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            albumId = data.get("albumID")
            songId = data.get("songID")
            if not albumId or not songId or albumId == "" or songId == "":
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            result, error = AlbumSongService.doHardDelete(
                albumId=albumId, songId=songId
            )
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Không tồn tại")
                elif error == ErrorCodes.DELETE_FAILED:
                    return BaseResponse.internalError("Xóa thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", AlbumSongSerializer(result).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
