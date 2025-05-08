from django.views import View
from app.services.albumsService import AlbumsService
from app.entities.albums import Albums
from app.serializers.albumsSerializer import AlbumsSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json
import logging

logger = logging.getLogger(__name__)

class GetAlbums(View):
    def get(self, request, id=None):
        try:
            page = int(request.GET.get("page", "1"))
            pageSize = int(request.GET.get("pageSize", "10"))

            if id:
                result, error = AlbumsService.findById(id)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Album không tồn tại", str(error))
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", AlbumsSerializer(result).data)
            else:
                if not page or not pageSize:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            result, error = AlbumsService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Không tìm thấy album")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': AlbumsSerializer(result['result'], many=True).data,
                'total': result['total'],
                'totalPages': result['totalPages'],
                'currentPage': result['currentPage']
            })
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
    
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get("name")
            page = int(data.get("page", "1"))
            pageSize = int(data.get("pageSize", "10"))

            if not page or not pageSize:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")
            
            if not name or name == "":
                result, error = AlbumsService.findAllPaginated(page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Không tìm thấy album")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': AlbumsSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })

            result, error = AlbumsService.findByNamePaginated(name, page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Không tìm thấy album")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': AlbumsSerializer(result['result'], many=True).data,
                'total': result['total'],
                'totalPages': result['totalPages'],
                'currentPage': result['currentPage']
            })

        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class CreateAlbum(View):
    def post(self, request):
        try:
            logger.info("Received album creation request")
            data = json.loads(request.body.decode('utf-8'))
            name = data.get("name")
            description = data.get("description")
            storageImageId = data.get("storageImageId")
            artistId = data.get("artistId")

            logger.info(f"Album creation data - name: {name}, artistId: {artistId}, storageImageId: {storageImageId}")

            if not name or not description or not storageImageId or not artistId:
                logger.warning("Invalid album creation data - missing required fields")
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            album, error = AlbumsService.doCreate(name=name, artistId=artistId, description=description, storageImageId=storageImageId)
            if error:
                logger.error(f"Album creation failed with error: {error}")
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.ALREADY_EXISTS:
                    return BaseResponse.badRequest("Album đã tồn tại")
                elif error == ErrorCodes.CREATE_FAILED:
                    return BaseResponse.internalError("Tạo album thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            
            logger.info(f"Album created successfully with ID: {album.id}")
            return BaseResponse.success("Thành công", AlbumsSerializer(album).data)
        except Exception as e:
            logger.error(f"Unexpected error in album creation: {str(e)}", exc_info=True)
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class UpdateAlbum(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            name = data.get("name")
            description = data.get("description")
            storageImageId = data.get("storageImageId")

            if not id or not name or not description or not storageImageId:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            album, error = AlbumsService.doUpdate(id, name, description, storageImageId)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Album không tồn tại")
                elif error == ErrorCodes.UPDATE_FAILED:
                    return BaseResponse.internalError("Cập nhật album thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
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
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Album không tồn tại")
                elif error == ErrorCodes.DELETE_FAILED:
                    return BaseResponse.internalError("Xóa album thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", AlbumsSerializer(album).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))