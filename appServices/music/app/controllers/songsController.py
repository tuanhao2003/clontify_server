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
                    return BaseResponse.notFound("Bài hát không tồn tại", str(error))
                return BaseResponse.success("Thành công", SongsSerializer(result).data)
            
            if not page or not pageSize:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")
            result, error = SongsService.findAll(page, pageSize)
            if error:
                return BaseResponse.notFound("Chưa có bài hát nào", str(error))
            return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            title = data.get("title")
            artistId = data.get("artistId") 
            genreId = data.get("genreId")
            albumId = data.get("albumId")
            page = int(data.get("page", "1"))
            pageSize = int(data.get("pageSize", "10"))

            if title:
                result, error = SongsService.findByTitle(title, page, pageSize)
                if error:
                    return BaseResponse.notFound("Chưa có bài hát nào", str(error))
                return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)
                
            # if artistId:
            #     result, error = SongsService.findByArtistId(artistId, page, pageSize)
            #     if error:
            #         return BaseResponse.notFound("Chưa có bài hát nào", str(error))
            #     return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)
                
            if genreId:
                result, error = SongsService.findByGenreId(genreId)
                if error:
                    return BaseResponse.notFound("Chưa có bài hát nào", str(error))
                return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)
                
            if albumId:
                result, error = SongsService.findByAlbumId(albumId)
                if error:
                    return BaseResponse.notFound("Chưa có bài hát nào", str(error))
                return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)

            else:
                if not page or not pageSize:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                result, error = SongsService.findAll(page, pageSize)
                if error:
                    return BaseResponse.notFound("Chưa có bài hát nào", str(error))
                return BaseResponse.success("Thành công", SongsSerializer(result, many=True).data)
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class CreateSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            title = data.get("title")
            artistId = data.get("artistId")
            genreIds = data.get("genreId")
            audioUrl = data.get("audioUrl")
            backgroundImage = data.get("backgroundImage")
            duration = data.get("duration")
            description = data.get("description")
            albumIds = data.get("albumId")
            subArtistIds = data.get("subArtistId")

            if not title or not artistId or not albumIds or not audioUrl:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            song, error = SongsService.doCreate(title, artistId, audioUrl, albumIds, genreIds, backgroundImage, duration, description, subArtistIds)
            if error:
                return BaseResponse.internalError("Tạo bài hát thất bại", str(error))
            return BaseResponse.success("Thành công", SongsSerializer(song).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
        
class UpdateSong(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            title = data.get("title")
            backgroundImage = data.get("backgroundImage")
            duration = data.get("duration")
            description = data.get("description")
            
            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            song, error = SongsService.doUpdate(id, title, backgroundImage, duration, description)
            if error:
                return BaseResponse.internalError("Cập nhật bài hát thất bại", str(error))
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
                return BaseResponse.internalError("Xóa bài hát thất bại", str(error))
            return BaseResponse.success("Thành công", SongsSerializer(song).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))