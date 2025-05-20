from django.views import View
from app.services.songsService import SongsService
from app.entities.songs import Songs
from app.serializers.songsSerializer import SongsSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class GetSongs(View):
    def get(self, request, id=None):
        try:
            page = int(request.GET.get("page", "1"))
            pageSize = int(request.GET.get("pageSize", "10"))
            
            if id:
                result, error = SongsService.findById(id)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Bài hát không tồn tại")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", SongsSerializer(result).data)
            elif len(ids := request.GET.getlist("ids[]", [])) > 0:
                result, error = SongsService.findByIds(ids)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Bài hát không tồn tại")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)
            
            if not page or not pageSize:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")
            result, error = SongsService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Chưa có bài hát nào")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': SongsSerializer(result['result'], many=True).data,
                'total': result['total'],
                'totalPages': result['totalPages'],
                'currentPage': result['currentPage']
            })
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            title = data.get("title")
            artistId = data.get("artistId") 
            genreId = data.get("genreId")
            albumId = data.get("albumId")
            songType = data.get("songType")
            page = int(data.get("page", "1"))
            pageSize = int(data.get("pageSize", "10"))

            if not page or not pageSize:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            if title:
                result, error = SongsService.findByTitlePaginated(title, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có bài hát nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': SongsSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })
                
            if artistId:
                result, error = SongsService.findByArtistIdPaginated(artistId, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có bài hát nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': SongsSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })
                
            if genreId:
                result, error = SongsService.findByGenreIdPaginated(genreId, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có bài hát nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': SongsSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })
                
            if albumId:
                result, error = SongsService.findByAlbumIdPaginated(albumId, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có bài hát nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': SongsSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })

            if songType:
                result, error = SongsService.findBySongTypePaginated(songType, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có bài hát nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': SongsSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })

            result, error = SongsService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Chưa có bài hát nào")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': SongsSerializer(result['result'], many=True).data,
                'total': result['total'],
                'totalPages': result['totalPages'],
                'currentPage': result['currentPage']
            })
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class CreateSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            title = data.get("title")
            artistId = data.get("artistId")
            genreIds = data.get("genreId")
            storageId = data.get("storageId")
            storageImageId = data.get("storageImageId")
            duration = data.get("duration")
            description = data.get("description")
            albumIds = data.get("albumId")
            subArtistIds = data.get("subArtistId")
            songType = data.get("songType")

            if not title or not artistId or not albumIds or not storageId or not songType:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            song, error = SongsService.doCreate(title, artistId, storageId, albumIds, songType, genreIds, storageImageId, duration, description, subArtistIds)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.ALREADY_EXISTS:
                    return BaseResponse.badRequest("Bài hát đã tồn tại")
                elif error == ErrorCodes.CREATE_FAILED:
                    return BaseResponse.internalError("Tạo bài hát thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", SongsSerializer(song).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
        
class UpdateSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            title = data.get("title")
            storageImageId = data.get("storageImageId")
            duration = data.get("duration")
            description = data.get("description")
            songType = data.get("songType")
            removeImage = data.get("removeImage")
            
            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            song, error = SongsService.doUpdate(id, title, storageImageId, duration, description, songType, removeImage)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Bài hát không tồn tại")
                elif error == ErrorCodes.UPDATE_FAILED:
                    return BaseResponse.internalError("Cập nhật bài hát thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", SongsSerializer(song).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class DeleteSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")
            
            song, error = SongsService.doDelete(id)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Bài hát không tồn tại")
                elif error == ErrorCodes.DELETE_FAILED:
                    return BaseResponse.internalError("Xóa bài hát thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", SongsSerializer(song).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))