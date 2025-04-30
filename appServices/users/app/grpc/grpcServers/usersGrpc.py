import grpc
from concurrent import futures
import time
import uuid
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import userService_pb2, userService_pb2_grpc
from app.services.profilesService import ProfilesService
from app.serializer.profileSerializer import ProfileSerializer
from common.errorCodes import ErrorCodes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class UsersGrpc(userService_pb2_grpc.UserServiceServicer):
    def _authenticate(self, context):
        token = None
        for key, value in context.invocation_metadata():
            if key == 'authorization':
                if value.startswith('Bearer '):
                    token = value[7:]
                else:
                    token = value
        if not token:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Missing JWT token")
            return None
        try:
            validated = JWTAuthentication().get_validated_token(token)
            user = JWTAuthentication().get_user(validated)
            return user
        except Exception as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid JWT token: " + str(e))
            return None

    def GetProfile(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            profile, error = ProfilesService.findByID(request.id)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID format")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Profile not found")
                return None
            return userService_pb2.GetProfileResponse(
                profile=userService_pb2.Profile(
                    id=str(profile.id),
                    accountID=str(profile.accountID),
                    fullName=profile.fullName,
                    avatarUrl=profile.avatarUrl,
                    bio=profile.bio,
                    dateOfBirth=profile.dateOfBirth.isoformat() if profile.dateOfBirth else "",
                    phoneNumber=profile.phoneNumber,
                    createdAt=Timestamp(seconds=int(profile.createdAt.timestamp())),
                    updatedAt=Timestamp(seconds=int(profile.updatedAt.timestamp())),
                    deletedAt=Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                    isActive=profile.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def GetProfileByAccountID(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            profile, error = ProfilesService.findByAccountID(request.accountID)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid account ID format")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Profile not found")
                return None
            return userService_pb2.GetProfileByAccountIDResponse(
                profile=userService_pb2.Profile(
                    id=str(profile.id),
                    accountID=str(profile.accountID),
                    fullName=profile.fullName,
                    avatarUrl=profile.avatarUrl,
                    bio=profile.bio,
                    dateOfBirth=profile.dateOfBirth.isoformat() if profile.dateOfBirth else "",
                    phoneNumber=profile.phoneNumber,
                    createdAt=Timestamp(seconds=int(profile.createdAt.timestamp())),
                    updatedAt=Timestamp(seconds=int(profile.updatedAt.timestamp())),
                    deletedAt=Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                    isActive=profile.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def CreateProfile(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            profile, error = ProfilesService.doCreate(
                accountID=request.accountID,
                fullName=request.fullName,
                avatarUrl=request.avatarUrl,
                bio=request.bio,
                dateOfBirth=request.dateOfBirth,
                phoneNumber=request.phoneNumber
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Missing required fields")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Profile already exists")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create profile")
                return None
            return userService_pb2.CreateProfileResponse(
                profile=userService_pb2.Profile(
                    id=str(profile.id),
                    accountID=str(profile.accountID),
                    fullName=profile.fullName,
                    avatarUrl=profile.avatarUrl,
                    bio=profile.bio,
                    dateOfBirth=profile.dateOfBirth.isoformat() if profile.dateOfBirth else "",
                    phoneNumber=profile.phoneNumber,
                    createdAt=Timestamp(seconds=int(profile.createdAt.timestamp())),
                    updatedAt=Timestamp(seconds=int(profile.updatedAt.timestamp())),
                    deletedAt=Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                    isActive=profile.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def UpdateProfile(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            data = {
                "id": request.id,
                "fullName": request.fullName,
                "avatarUrl": request.avatarUrl,
                "bio": request.bio,
                "dateOfBirth": request.dateOfBirth,
                "phoneNumber": request.phoneNumber
            }
            profile, error = ProfilesService.doUpdate(ProfileSerializer.deserialize(data))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Missing required fields")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Profile not found")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to update profile")
                return None
            return userService_pb2.UpdateProfileResponse(
                profile=userService_pb2.Profile(
                    id=str(profile.id),
                    accountID=str(profile.accountID),
                    fullName=profile.fullName,
                    avatarUrl=profile.avatarUrl,
                    bio=profile.bio,
                    dateOfBirth=profile.dateOfBirth.isoformat() if profile.dateOfBirth else "",
                    phoneNumber=profile.phoneNumber,
                    createdAt=Timestamp(seconds=int(profile.createdAt.timestamp())),
                    updatedAt=Timestamp(seconds=int(profile.updatedAt.timestamp())),
                    deletedAt=Timestamp(seconds=int(profile.deletedAt.timestamp())) if profile.deletedAt else None,
                    isActive=profile.isActive
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def DeleteProfile(self, request, context):
        user = self._authenticate(context)
        if not user:
            return userService_pb2.DeleteProfileResponse(success=False, message="Unauthenticated")
        try:
            result, error = ProfilesService.doDelete(request.id)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID format")
                return userService_pb2.DeleteProfileResponse(success=False, message="Invalid ID format")
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Profile not found")
                return userService_pb2.DeleteProfileResponse(success=False, message="Profile not found")
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete profile")
                return userService_pb2.DeleteProfileResponse(success=False, message="Failed to delete profile")
            return userService_pb2.DeleteProfileResponse(success=True, message="Profile deleted successfully")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return userService_pb2.DeleteProfileResponse(success=False, message=str(e))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    userService_pb2_grpc.add_UserServiceServicer_to_server(UsersGrpc(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0) 