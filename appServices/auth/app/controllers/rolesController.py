from django.views import View
from app.services.rolesService import RolesService
from app.serializers.rolesSerializer import RolesSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json

class GetRoles(View):
    def get(self, request, id=None):
        try:
            page = int(request.GET.get("page", "1"))
            pageSize = int(request.GET.get("pageSize", "10"))
            
            if id:
                result, error = RolesService.findById(id)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Vai trò không tồn tại", str(error))
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", RolesSerializer(result).data)
            
            if not page or not pageSize:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
            result, error = RolesService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Chưa có vai trò nào", str(error))
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': RolesSerializer(result['result'], many=True).data,
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
                return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))

            if name:
                result, error = RolesService.findByNamePaginated(name, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có vai trò nào", str(error))
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': RolesSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })

            result, error = RolesService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Chưa có vai trò nào", str(error))
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': RolesSerializer(result['result'], many=True).data,
                'total': result['total'],
                'totalPages': result['totalPages'],
                'currentPage': result['currentPage']
            })
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class CreateRole(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            name = data.get("name")
            description = data.get("description")

            if not name:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))

            role, error = RolesService.doCreate(name, description)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
                elif error == ErrorCodes.ALREADY_EXISTS:
                    return BaseResponse.badRequest("Vai trò đã tồn tại", str(error))
                elif error == ErrorCodes.CREATE_FAILED:
                    return BaseResponse.internalError("Tạo vai trò thất bại", str(error))
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", RolesSerializer(role).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class UpdateRole(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            name = data.get("name")
            description = data.get("description")

            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))

            role, error = RolesService.doUpdate(id, name, description)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Vai trò không tồn tại", str(error))
                elif error == ErrorCodes.ALREADY_EXISTS:
                    return BaseResponse.badRequest("Tên vai trò đã tồn tại", str(error))
                elif error == ErrorCodes.UPDATE_FAILED:
                    return BaseResponse.internalError("Cập nhật vai trò thất bại", str(error))
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", RolesSerializer(role).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class DeleteRole(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
            
            role, error = RolesService.doDelete(id)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ", str(error))
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Vai trò không tồn tại", str(error))
                elif error == ErrorCodes.DELETE_FAILED:
                    return BaseResponse.internalError("Xóa vai trò thất bại", str(error))
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", RolesSerializer(role).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e)) 