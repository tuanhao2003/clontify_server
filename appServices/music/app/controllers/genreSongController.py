from django.views import View
from app.services.genreSongService import GenreSongService
from app.serializers.genreSongSerializer import GenreSongSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json


class GetGenreSong(View):

    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            genreId = data.get("genreID")
            songId = data.get("songID")
            page = int(data.get("page", "1"))
            pageSize = int(data.get("pageSize", "10"))

            if genreId and songId:
                result, error = GenreSongService.findExactly(
                    genreId=genreId, songId=songId
                )
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Không tìm thấy")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success(
                    "Thành công", GenreSongSerializer(result).data
                )

            if genreId and genreId != "":
                result, error = GenreSongService.findByGenreIdPaginated(
                    genreId, page, pageSize
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
                        "result": GenreSongSerializer(result["result"], many=True).data,
                        "total": result["total"],
                        "totalPages": result["totalPages"],
                        "currentPage": result["currentPage"],
                    },
                )

            if songId and songId != "":
                result, error = GenreSongService.findBySongIdPaginated(
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
                        "result": GenreSongSerializer(result["result"], many=True).data,
                        "total": result["total"],
                        "totalPages": result["totalPages"],
                        "currentPage": result["currentPage"],
                    },
                )

            result, error = GenreSongService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Không tìm thấy genre")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success(
                "Thành công",
                {
                    "result": GenreSongSerializer(result["result"], many=True).data,
                    "total": result["total"],
                    "totalPages": result["totalPages"],
                    "currentPage": result["currentPage"],
                },
            )

        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))


class CreateGenreSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            genreId = data.get("genreID")
            songId = data.get("songID")

            if not genreId or not songId or genreId == "" or songId == "":
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            result, error = GenreSongService.doCreate(genreId=genreId, songId=songId)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.ALREADY_EXISTS:
                    return BaseResponse.badRequest("Đã tồn tại")
                elif error == ErrorCodes.CREATE_FAILED:
                    return BaseResponse.internalError("Tạo thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))

            return BaseResponse.success("Thành công", GenreSongSerializer(result).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))


class DeleteGenreSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            genreId = data.get("genreID")
            songId = data.get("songID")
            if not genreId or not songId or genreId == "" or songId == "":
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            result, error = GenreSongService.doHardDelete(
                genreId=genreId, songId=songId
            )
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Không tồn tại")
                elif error == ErrorCodes.DELETE_FAILED:
                    return BaseResponse.internalError("Xóa thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", GenreSongSerializer(result).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
