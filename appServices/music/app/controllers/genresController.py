from django.views import View
from app.services.genresService import GenresService
from app.entities.genres import Genres
from app.serializers.genresSerializer import GenresSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class GetGenres(View):
    def get(self, request, id=None):
        try:
            page = int(request.GET.get("page", "1"))
            pageSize = int(request.GET.get("pageSize", "10"))

            if id:
                result, error = GenresService.findById(id)
                if error:
                    return BaseResponse.notFound("Thể loại không tồn tại", str(error))
                return BaseResponse.success("Thành công", GenresSerializer(result).data)
            else:
                if not page or not pageSize:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            result, error = GenresService.findAll(page, pageSize)
            if error:
                return BaseResponse.notFound("Không tìm thấy thể loại", str(error))
            return BaseResponse.success("Thành công", GenresSerializer(result, many=True).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get("name")
            songId = data.get("songId")
            page = int(data.get("page", "1"))
            pageSize = int(data.get("pageSize", "10"))

            if name:
                result, error = GenresService.findByName(name, page, pageSize)
                if error:
                    return BaseResponse.notFound("Không tìm thấy thể loại", str(error))
                return BaseResponse.success("Thành công", GenresSerializer(result, many=True).data)
            
            if songId:
                result, error = GenresService.findBySongId(songId, page, pageSize)
                if error:
                    return BaseResponse.notFound("Không tìm thấy thể loại", str(error))
                return BaseResponse.success("Thành công", GenresSerializer(result, many=True).data)
            
            else:
                if not page or not pageSize:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            result, error = GenresService.findAll(page, pageSize)
            if error:
                return BaseResponse.notFound("Không tìm thấy thể loại", str(error))
            return BaseResponse.success("Thành công", GenresSerializer(result, many=True).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class CreateGenre(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get("name")
            description = data.get("description")

            if not name or name == "":
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            genre, error = GenresService.doCreate(name, description)
            if error:
                return BaseResponse.internalError("Tạo thể loại thất bại", str(error))
            return BaseResponse.success("Thành công", GenresSerializer(genre).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
        
class UpdateGenre(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            name = data.get("name")
            description = data.get("description")

            if not id or not name or name == "":
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            genre, error = GenresService.doUpdate(id, name, description)
            if error:
                return BaseResponse.internalError("Cập nhật thể loại thất bại", str(error))
            return BaseResponse.success("Thành công", GenresSerializer(genre).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
        
class DeleteGenre(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            genre, error = GenresService.doDelete(id)
            if error:
                return BaseResponse.internalError("Xóa thể loại thất bại", str(error))
            return BaseResponse.success("Thành công", GenresSerializer(genre).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))