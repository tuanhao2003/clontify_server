import grpc
from app.grpc.protos import userService_pb2, userService_pb2_grpc
from common.errorCodes import ErrorCodes

# log
import logging
log = logging.getLogger(__name__)

class UsersGrpcClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = userService_pb2_grpc.UserServiceStub(self.channel)

    def getProfileByAccountID(self, accountID, token=None):
        try:
            request = userService_pb2.GetProfileByAccountIDRequest(
                accountID=str(accountID)
            )
            metadata = []
            if token:
                metadata.append(('authorization', f'Bearer {token}'))
            response = self.stub.GetProfileByAccountID(request, metadata=metadata)
            return response.profile, None
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                return None, ErrorCodes.INVALID_INPUT
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None, ErrorCodes.NOT_FOUND
            return None, ErrorCodes.OPERATION_FAILED

    def createProfile(self, accountID, fullName="noname", avatarUrl=None, bio=None, dateOfBirth=None, phoneNumber=None, token=None):
        try:
            request = userService_pb2.CreateProfileRequest(
                accountID=str(accountID),
                fullName=fullName,
                avatarUrl=avatarUrl if avatarUrl else "",
                bio=bio if bio else "",
                dateOfBirth=dateOfBirth.isoformat() if dateOfBirth else "",
                phoneNumber=phoneNumber if phoneNumber else ""
            )
            metadata = []
            if token:
                metadata.append(('authorization', f'Bearer {token}'))
            response = self.stub.CreateProfile(request, metadata=metadata)
            return response.profile, None
        except grpc.RpcError as e:
            log.error(str(e))
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                return None, ErrorCodes.INVALID_INPUT
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                return None, ErrorCodes.ALREADY_EXISTS
            return None, ErrorCodes.CREATE_FAILED

    def updateProfile(self, id, fullName=None, avatarUrl=None, bio=None, dateOfBirth=None, phoneNumber=None, token=None):
        try:
            request = userService_pb2.UpdateProfileRequest(
                id=str(id),
                fullName=fullName if fullName else "",
                avatarUrl=avatarUrl if avatarUrl else "",
                bio=bio if bio else "",
                dateOfBirth=dateOfBirth.isoformat() if dateOfBirth else "",
                phoneNumber=phoneNumber if phoneNumber else ""
            )
            metadata = []
            if token:
                metadata.append(('authorization', f'Bearer {token}'))
            response = self.stub.UpdateProfile(request, metadata=metadata)
            return response.profile, None
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                return None, ErrorCodes.INVALID_INPUT
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None, ErrorCodes.NOT_FOUND
            return None, ErrorCodes.UPDATE_FAILED

    def deleteProfile(self, id, token=None):
        try:
            request = userService_pb2.DeleteProfileRequest(
                id=str(id)
            )
            metadata = []
            if token:
                metadata.append(('authorization', f'Bearer {token}'))
            response = self.stub.DeleteProfile(request, metadata=metadata)
            if not response.success:
                return None, ErrorCodes.DELETE_FAILED
            return response, None
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                return None, ErrorCodes.INVALID_INPUT
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None, ErrorCodes.NOT_FOUND
            return None, ErrorCodes.DELETE_FAILED

    def close(self):
        self.channel.close() 