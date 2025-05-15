from django.views import View
from app.services.profilesService import ProfilesService
from app.serializers.profileSerializer import ProfileSerializer
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
import json
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.utils.timezone import now


class GetProfile(View):
    def get(self, request, id=None):
        authHeader = request.headers.get("Authorization")
        accountID = None
        if authHeader and authHeader.startswith("Bearer "):
            tokenStr = authHeader.split(" ")[1]
            try:
                token = AccessToken(tokenStr)
                accountID = token.get("user_id")
            except (TokenError, InvalidToken):
                return BaseResponse.invalidToken("Token không hợp lệ")
            
        if id is not None:
            result, error = ProfilesService.findByID(id)
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy hồ sơ")
            return BaseResponse.success("Thành công", ProfileSerializer(result).data)

        if accountID:
            result, error = ProfilesService.findByAccountID(str(accountID))
            if error == ErrorCodes.INVALID_INPUT:
                return BaseResponse.badRequest("Thiếu ID tài khoản")
            if error == ErrorCodes.NOT_FOUND:
                return BaseResponse.notFound("Không tìm thấy hồ sơ")
            return BaseResponse.success("Thành công", ProfileSerializer(result).data)
        
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        fullName = data.get("email")
        date = data.get("date")

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
    
class UpdateProfile(View):
    def post(self, request):
        authHeader = request.headers.get("Authorization")
        accountID = None
        if authHeader and authHeader.startswith("Bearer "):
            tokenStr = authHeader.split(" ")[1]
            try:
                token = AccessToken(tokenStr)
                accountID = token.get("user_id")
            except (TokenError, InvalidToken):
                return BaseResponse.invalidToken("Token không hợp lệ")
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return BaseResponse.badRequest("Dữ liệu không hợp lệ")
        
        profile, error = ProfilesService.findByAccountID(accountID)
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("dữl liệu không hợp lệ")
        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Không tìm thấy hồ sơ")
        
        profile.fullName = data.get("fullName")
        profile.dateOfBirth = data.get("dateOfBirth")
        profile.bio = data.get("bio")
        profile.phoneNumber = data.get("phoneNumber")
        profile.avatarUrl = data.get("avatarUrl")

        result, error = ProfilesService.doUpdate(profile)
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("Thiếu ID")
        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Không tìm thấy hồ sơ")
        if error == ErrorCodes.UPDATE_FAILED:
            return BaseResponse.updateFailed("Cập nhật thất bại")
        return BaseResponse.success("Cập nhật thành công", ProfileSerializer(result).data)


class DeleteProfile(View):
    def post(self, request):
        authHeader = request.headers.get("Authorization")
        accountID = None
        if authHeader and authHeader.startswith("Bearer "):
            tokenStr = authHeader.split(" ")[1]
            try:
                token = AccessToken(tokenStr)
                accountID = token.get("user_id")
            except (TokenError, InvalidToken):
                return BaseResponse.invalidToken("Token không hợp lệ")
        
        profile, error = ProfilesService.findByAccountID(accountID)
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("dữl liệu không hợp lệ")
        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Không tìm thấy hồ sơ")

        result, error = ProfilesService.doDelete(profile.id)
        if error == ErrorCodes.INVALID_INPUT:
            return BaseResponse.badRequest("Thiếu ID")
        if error == ErrorCodes.NOT_FOUND:
            return BaseResponse.notFound("Không tìm thấy hồ sơ")
        if error == ErrorCodes.DELETE_FAILED:
            return BaseResponse.internalServerError("Xóa thất bại")
        return BaseResponse.success("Xoá thành công")