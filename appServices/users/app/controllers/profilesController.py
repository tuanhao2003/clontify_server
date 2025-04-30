from django.views import View
from app.services.profilesService import ProfilesService
from app.serializer.profileSerializer import ProfileSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json
from datetime import datetime


class GetProfile(View):
    def get(self, request):
        id = request.GET.get("id")
        accountID = request.GET.get("accountID") 
        fullName = request.GET.get("fullName")
        date = request.GET.get("date")

        if id:
            result, error = ProfilesService.findByID(id)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy hồ sơ")
            return BaseResponse.success("Thành công", ProfileSerializer(result).data)

        if accountID:
            result, error = ProfilesService.findByAccountID(accountID)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID tài khoản")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy hồ sơ")
            return BaseResponse.success("Thành công", ProfileSerializer(result).data)

        if fullName:
            result, error = ProfilesService.findByFullName(fullName)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu tên đầy đủ")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy hồ sơ")
            return BaseResponse.success("Thành công", ProfileSerializer(result).data)

        if date:
            result, error = ProfilesService.findByDateOfBirth(date)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Ngày không hợp lệ")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy hồ sơ nào")
            return BaseResponse.success("Thành công", ProfileSerializer(result, many=True).data)

        return BaseResponse.badRequest("Không có tham số nào hợp lệ")


class CreateProfile(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        accountID = data.get("accountID")
        fullName = data.get("fullName")
        avatarUrl = data.get("avatarUrl")
        bio = data.get("bio")
        dateOfBirth = data.get("dateOfBirth")
        phoneNumber = data.get("phoneNumber")

        result, error = ProfilesService.doCreate(
            accountID=accountID,
            fullName=fullName,
            avatarUrl=avatarUrl,
            bio=bio,
            dateOfBirth=dateOfBirth,
            phoneNumber=phoneNumber
        )

        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("Thiếu thông tin bắt buộc")
        if error == ErrorCodes.ALREADY_EXISTS:
            return BaseResponse.badRequest("Hồ sơ đã tồn tại")
        if error == ErrorCodes.CREATE_FAILED:
            return BaseResponse.internalServerError("Tạo hồ sơ thất bại")
        return BaseResponse.success("Tạo thành công", ProfileSerializer(result).data)


class UpdateProfile(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        result, error = ProfilesService.doUpdate(ProfileSerializer.deserialize(data))
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("Thiếu ID")
        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Không tìm thấy hồ sơ")
        if error == ErrorCodes.UPDATE_FAILED:
            return BaseResponse.internalServerError("Cập nhật thất bại")
        return BaseResponse.success("Cập nhật thành công", ProfileSerializer(result).data)


class DeleteProfile(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")

        id = data.get("id")
        result, error = ProfilesService.doDelete(id)
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("Thiếu ID")
        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Không tìm thấy hồ sơ")
        if error == ErrorCodes.DELETE_FAILED:
            return BaseResponse.internalServerError("Xóa thất bại")
        return BaseResponse.success("Xoá thành công")