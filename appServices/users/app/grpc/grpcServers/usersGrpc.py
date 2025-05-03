import grpc
from concurrent import futures
import time
import uuid
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import userService_pb2, userService_pb2_grpc
from app.services.profilesService import ProfilesService
from common.errorCodes import ErrorCodes

class AuthGrpc(userService_pb2_grpc.UserServiceServicer):

    def findByID(self, request, context):
        try:
            profile, error = ProfilesService.findByID(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy profile")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None

            return userService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp(seconds=int(profile.createdAt.timestamp())),
                updatedAt = Timestamp(seconds=int(profile.updatedAt.timestamp())),
                deletedAt = Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
    
    def findByAccountID(self, request, context):
        try:
            profile, error = ProfilesService.findByAccountID(uuid.UUID(request.accountID))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("accountID không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy profile")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None

            return userService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp(seconds=int(profile.createdAt.timestamp())),
                updatedAt = Timestamp(seconds=int(profile.updatedAt.timestamp())),
                deletedAt = Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        
    def doCreate(self, request, context):
        try:
            accountID = uuid.UUID(request.accountID)
            fullName = request.fullName
            avatarUrl = request.avatarUrl
            bio = request.bio
            dateOfBirth = request.dateOfBirth
            phoneNumber = request.phoneNumber

            profile, error = ProfilesService.doCreate(accountID,fullName,avatarUrl,bio,dateOfBirth,phoneNumber)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Dữ liệu không hợp lệ")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Profile đã tồn tại")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi khi tạo profile")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None

            return userService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp(seconds=int(profile.createdAt.timestamp())),
                updatedAt = Timestamp(seconds=int(profile.updatedAt.timestamp())),
                deletedAt = Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None
        
    def doUpdate(self, request, context):
        try:
            id = uuid.UUID(request.id)
            fullName = request.fullName
            avatarUrl = request.avatarUrl
            bio = request.bio
            dateOfBirth = request.dateOfBirth
            phoneNumber = request.phoneNumber

            baseProfile, baseError = ProfilesService.findByID(id)
            if baseError == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("accountID không hợp lệ")
                return None
            if baseError == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy profile")
                return None
            if baseError:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None

            baseProfile.fullName = fullName
            baseProfile.avatarUrl = avatarUrl
            baseProfile.bio = bio
            baseProfile.dateOfBirth = dateOfBirth
            baseProfile.phoneNumber = phoneNumber
            profile, error = ProfilesService.doUpdate(baseProfile)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Dữ liệu không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy profile")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi khi cập nhật profile")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None

            return userService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp(seconds=int(profile.createdAt.timestamp())),
                updatedAt = Timestamp(seconds=int(profile.updatedAt.timestamp())),
                deletedAt = Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def doDelete(self, request, context):
        try:
            profile, error = ProfilesService.doDelete(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Xóa thất bại")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None

            return userService_pb2.ProfileResponse(
                id = str(profile.id),
                accountID = profile.accountID,
                fullName = profile.fullName,
                avatarUrl = profile.avatarUrl,
                bio = profile.bio,
                dateOfBirth = profile.dateOfBirth,
                phoneNumber = profile.phoneNumber,
                createdAt = Timestamp(seconds=int(profile.createdAt.timestamp())),
                updatedAt = Timestamp(seconds=int(profile.updatedAt.timestamp())),
                deletedAt = Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                isActive = profile.isActive,
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    userService_pb2_grpc.add_UserServiceServicer_to_server(AuthGrpc(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
