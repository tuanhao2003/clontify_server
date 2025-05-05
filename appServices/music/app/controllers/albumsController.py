from django.views import View
from app.services.albumsService import AlbumsService
from app.entities.albums import Albums
from app.serializers.albumsSerializer import AlbumsSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class GetAlbums(View):
    def get(self, request, id=None):
        try:
            page = int(request.GET.get("page", "1"))
            pageSize = int(request.GET.get("pageSize", "10"))

            if id:
                result, error = AlbumsService.findById(id)
                if error:
                    return BaseResponse.notFound("Album không tồn tại", str(error))
                return BaseResponse.success("Thành công", AlbumsSerializer(result).data)
            else:
                if not page or not pageSize:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            result, error = AlbumsService.findAll(page, pageSize)
            if error:
                return BaseResponse.notFound("Không tìm thấy album", str(error))
            return BaseResponse.success("Thành công", AlbumsSerializer(result, many=True).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
    
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get("name")
            description = data.get("description")
            backgroundImage = data.get("backgroundImage")
            
        except Exception as e:

class CreateAlbum(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get("name")
            description = data.get("description")
            backgroundImage = data.get("backgroundImage")

            if not name or not description or not backgroundImage:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            album, error = AlbumsService.doCreate(name, description, backgroundImage)
            if error:
                return BaseResponse.internalError("Tạo album thất bại", str(error))
            return BaseResponse.success("Thành công", AlbumsSerializer(album).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class UpdateAlbum(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            name = data.get("name")
            description = data.get("description")
            backgroundImage = data.get("backgroundImage")

            if not id or not name or not description or not backgroundImage:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            album, error = AlbumsService.doUpdate(id, name, description, backgroundImage)
            if error:
                return BaseResponse.internalError("Cập nhật album thất bại", str(error))
            return BaseResponse.success("Thành công", AlbumsSerializer(album).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class DeleteAlbum(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            album, error = AlbumsService.doDelete(id)
            if error:
                return BaseResponse.internalError("Xóa album thất bại", str(error))
            return BaseResponse.success("Thành công", AlbumsSerializer(album).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))