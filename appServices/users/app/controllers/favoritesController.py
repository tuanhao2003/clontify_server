from django.views import View
from app.services.favoritesService import FavoritesService
from app.entities.favorites import Favorites
from app.serializers.favoritesSerializer import FavoritesSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class GetFavorites(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            profileId = data.get("profileId")
            songId = data.get("songId")
            page = int(data.get("page", "1"))
            pageSize = int(data.get("pageSize", "10"))

            if not page or not pageSize:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            if profileId:
                result, error = FavoritesService.findByProfileIdPaginated(profileId, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có yêu thích nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': FavoritesSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })
                
            if songId:
                result, error = FavoritesService.findBySongIdPaginated(songId, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có yêu thích nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': FavoritesSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })

            result, error = FavoritesService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Chưa có yêu thích nào")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': FavoritesSerializer(result['result'], many=True).data,
                'total': result['total'],
                'totalPages': result['totalPages'],
                'currentPage': result['currentPage']
            })
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class CreateFavorite(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            profileId = data.get("profileId")
            songId = data.get("songId")

            if not profileId or not songId:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            favorite, error = FavoritesService.doCreate(profileId, songId)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Bài hát không tồn tại")
                elif error == ErrorCodes.CREATE_FAILED:
                    return BaseResponse.internalError("Tạo yêu thích thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", FavoritesSerializer(favorite).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
        
class UpdateFavorite(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            profileId = data.get("profileId")
            songId = data.get("songId")
            isActive = data.get("isActive")

            if not profileId or not songId:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            favorite, error = FavoritesService.doUpdate(profileId, songId, isActive)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Bài hát không tồn tại")
                elif error == ErrorCodes.CREATE_FAILED:
                    return BaseResponse.internalError("Tạo yêu thích thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", FavoritesSerializer(favorite).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class DeleteFavorite(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            profileId = data.get("profileId")
            songId = data.get("songId")
            
            if not profileId or not songId:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")
            
            favorite, error = FavoritesService.doDelete(profileId, songId)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Yêu thích không tồn tại")
                elif error == ErrorCodes.DELETE_FAILED:
                    return BaseResponse.internalError("Xóa yêu thích thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", FavoritesSerializer(favorite).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e)) 