from django.views import View
from app.services.storageDataService import StorageDataService
from app.entities.storageData import StorageData
from app.serializers.storageDataSerializer import StorageDataSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json
from app.enums.fileTypeEnums import FileTypeEnums

class GetStorageData(View):
    def get(self, request, id=None):
        try:
            page = int(request.GET.get("page", "1"))
            pageSize = int(request.GET.get("pageSize", "10"))
            
            if id:
                result, error = StorageDataService.findById(id)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Dữ liệu không tồn tại")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", StorageDataSerializer(result).data)
            
            if not page or not pageSize:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")
            result, error = StorageDataService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Chưa có dữ liệu nào")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': StorageDataSerializer(result['result'], many=True).data,
                'total': result['total'],
                'totalPages': result['totalPages'],
                'currentPage': result['currentPage']
            })
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            fileName = data.get("fileName")
            userId = data.get("userId")
            fileType = data.get("fileType")
            page = int(data.get("page", "1"))
            pageSize = int(data.get("pageSize", "10"))

            if not page or not pageSize:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            if fileName:
                result, error = StorageDataService.findByFileNamePaginated(fileName, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có dữ liệu nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': StorageDataSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })
                
            if userId:
                result, error = StorageDataService.findByUserIdPaginated(userId, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có dữ liệu nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': StorageDataSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })
                
            if fileType:
                result, error = StorageDataService.findByFileTypePaginated(fileType, page, pageSize)
                if error:
                    if error == ErrorCodes.INVALID_INPUT:
                        return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                    elif error == ErrorCodes.NOT_FOUND:
                        return BaseResponse.notFound("Chưa có dữ liệu nào")
                    return BaseResponse.internalError("Lỗi hệ thống", str(error))
                return BaseResponse.success("Thành công", {
                    'result': StorageDataSerializer(result['result'], many=True).data,
                    'total': result['total'],
                    'totalPages': result['totalPages'],
                    'currentPage': result['currentPage']
                })

            result, error = StorageDataService.findAllPaginated(page, pageSize)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Chưa có dữ liệu nào")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", {
                'result': StorageDataSerializer(result['result'], many=True).data,
                'total': result['total'],
                'totalPages': result['totalPages'],
                'currentPage': result['currentPage']
            })
            
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class UploadFile(View):
    def post(self, request):
        try:
            file = request.FILES.get('file')
            if not file:
                return BaseResponse.badRequest("Không tìm thấy file")

            fileName = file.name
            fileType = file.content_type

            if fileType == 'audio/mpeg':
                fileType = FileTypeEnums.AUDIO
            elif fileType == 'video/mp4':
                fileType = FileTypeEnums.VIDEO
            elif fileType in ['image/jpeg', 'image/png', 'image/gif']:
                fileType = FileTypeEnums.IMAGE
            else:
                return BaseResponse.badRequest("Chỉ chấp nhận file mp3, mp4 và hình ảnh (jpg, png, gif)")

            result, error = StorageDataService.uploadToS3(file, fileName, fileType)
            if error:
                return BaseResponse.internalError("Upload file thất bại", str(error))

            s3Key = result['key']
            s3Url = result['url']
            return BaseResponse.success("Upload thành công", {
                'fileName': s3Key,
                'fileType': fileType,
                'fileSize': file.size,
                'fileUrl': s3Url
            })
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class CreateStorageData(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            fileName = data.get('fileName')
            fileType = data.get('fileType')
            userId = data.get('userId')
            fileUrl = data.get('fileUrl')
            fileSize = data.get('fileSize')
            description = data.get('description')

            if not fileName or not fileType or not userId or not fileUrl:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            storageData, error = StorageDataService.doCreate(fileName=fileName, fileType=fileType, userId=userId, fileUrl=fileUrl, fileSize=fileSize, description=description)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.CREATE_FAILED:
                    return BaseResponse.internalError("Tạo dữ liệu thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", StorageDataSerializer(storageData).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))
        
class UpdateStorageData(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            fileName = data.get("fileName")
            fileType = data.get("fileType")
            fileSize = data.get("fileSize")
            fileUrl = data.get("fileUrl")
            description = data.get("description")

            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")

            storageData, error = StorageDataService.doUpdate(id=id, fileName=fileName, fileType=fileType, fileSize=fileSize, fileUrl=fileUrl, description=description)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Dữ liệu không tồn tại")
                elif error == ErrorCodes.UPDATE_FAILED:
                    return BaseResponse.internalError("Cập nhật dữ liệu thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", StorageDataSerializer(storageData).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e))

class DeleteStorageData(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            id = data.get("id")
            if not id:
                return BaseResponse.badRequest("Dữ liệu không hợp lệ")
            
            storageData, error = StorageDataService.doDelete(id)
            if error:
                if error == ErrorCodes.INVALID_INPUT:
                    return BaseResponse.badRequest("Dữ liệu không hợp lệ")
                elif error == ErrorCodes.NOT_FOUND:
                    return BaseResponse.notFound("Dữ liệu không tồn tại")
                elif error == ErrorCodes.DELETE_FAILED:
                    return BaseResponse.internalError("Xóa dữ liệu thất bại")
                return BaseResponse.internalError("Lỗi hệ thống", str(error))
            return BaseResponse.success("Thành công", StorageDataSerializer(storageData).data)
        except Exception as e:
            return BaseResponse.internalError("Lỗi hệ thống", str(e)) 