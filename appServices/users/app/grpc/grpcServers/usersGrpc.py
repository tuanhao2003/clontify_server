import grpc
from concurrent import futures
import time
import uuid
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import usersService_pb2, usersService_pb2_grpc
from app.services.profilesService import ProfilesService
from common.errorCodes import ErrorCodes
from datetime import datetime

class UsersGrpc(usersService_pb2_grpc.UsersServiceServicer):
    def _parseTimestamp(self, dt):
        if not dt or not isinstance(dt, datetime):
            return None
        timestamp = Timestamp()
        timestamp.FromDatetime(dt)
        return timestamp
    
    def _parseDatetime(self, timestamp):
        if not timestamp or not isinstance(timestamp, Timestamp):
            return None
        return timestamp.ToDatetime()

    def findByID(self, request, context):
        try:
            profile, error = ProfilesService.findByID(request.id)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return usersService_pb2.ProfileResponse()
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy profile")
                return usersService_pb2.ProfileResponse()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return usersService_pb2.ProfileResponse()

            return usersService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp().FromDatetime(profile.createdAt),
                updatedAt = Timestamp().FromDatetime(profile.updatedAt),
                deletedAt = Timestamp().FromDatetime(profile.deletedAt) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return usersService_pb2.ProfileResponse()
    
    def findByAccountID(self, request, context):
        try:
            profile, error = ProfilesService.findByAccountID(request.accountID)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("accountID không hợp lệ")
                return usersService_pb2.ProfileResponse()
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy profile")
                return usersService_pb2.ProfileResponse()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return usersService_pb2.ProfileResponse()

            return usersService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp().FromDatetime(profile.createdAt),
                updatedAt = Timestamp().FromDatetime(profile.updatedAt),
                deletedAt = Timestamp().FromDatetime(profile.deletedAt) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return usersService_pb2.ProfileResponse()
        
    def doCreate(self, request, context):
        try:
            accountID = request.accountID
            fullName = request.fullName
            avatarUrl = request.avatarUrl
            bio = request.bio
            dateOfBirth = self._parseDatetime(request.dateOfBirth)
            phoneNumber = request.phoneNumber

            profile, error = ProfilesService.doCreate(accountID,fullName,avatarUrl,bio,dateOfBirth,phoneNumber)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Dữ liệu không hợp lệ")
                return usersService_pb2.ProfileResponse()
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Profile đã tồn tại")
                return usersService_pb2.ProfileResponse()
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi khi tạo profile")
                return usersService_pb2.ProfileResponse()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return usersService_pb2.ProfileResponse()

            return usersService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = self._parseTimestamp(profile.createdAt),
                updatedAt = self._parseTimestamp(profile.updatedAt),
                deletedAt = self._parseTimestamp(profile.deletedAt),
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return usersService_pb2.ProfileResponse()
        
    def doUpdate(self, request, context):
        try:
            id = request.id
            fullName = request.fullName
            avatarUrl = request.avatarUrl
            bio = request.bio
            dateOfBirth = request.dateOfBirth
            phoneNumber = request.phoneNumber

            baseProfile, baseError = ProfilesService.findByID(id)
            if baseError == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("accountID không hợp lệ")
                return usersService_pb2.ProfileResponse()
            if baseError == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy profile")
                return usersService_pb2.ProfileResponse()
            if baseError:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return usersService_pb2.ProfileResponse()

            baseProfile.fullName = fullName
            baseProfile.avatarUrl = avatarUrl
            baseProfile.bio = bio
            baseProfile.dateOfBirth = dateOfBirth
            baseProfile.phoneNumber = phoneNumber
            profile, error = ProfilesService.doUpdate(baseProfile)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Dữ liệu không hợp lệ")
                return usersService_pb2.ProfileResponse()
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy profile")
                return usersService_pb2.ProfileResponse()
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi khi cập nhật profile")
                return usersService_pb2.ProfileResponse()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return usersService_pb2.ProfileResponse()

            return usersService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp().FromDatetime(profile.createdAt),
                updatedAt = Timestamp().FromDatetime(profile.updatedAt),
                deletedAt = Timestamp().FromDatetime(profile.deletedAt) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return usersService_pb2.ProfileResponse()

    def doDelete(self, request, context):
        try:
            profile, error = ProfilesService.doDelete(request.id)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return usersService_pb2.ProfileResponse()
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Xóa thất bại")
                return usersService_pb2.ProfileResponse()
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return usersService_pb2.ProfileResponse()

            return usersService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp().FromDatetime(profile.createdAt),
                updatedAt = Timestamp().FromDatetime(profile.updatedAt),
                deletedAt = Timestamp().FromDatetime(profile.deletedAt) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return usersService_pb2.ProfileResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    usersService_pb2_grpc.add_UsersServiceServicer_to_server(UsersGrpc(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
