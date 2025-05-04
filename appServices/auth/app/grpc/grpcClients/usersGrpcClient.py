import grpc
from django.conf import settings
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from app.grpc.protos import usersService_pb2, usersService_pb2_grpc
from common.errorCodes import ErrorCodes

class UsersGrpcClient:
    def __init__(self):
        self.host = getattr(settings, 'USERS_GRPC_HOST', 'users_service')
        self.port = getattr(settings, 'USERS_GRPC_PORT', '50051')
        self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
        self.stub = usersService_pb2_grpc.UsersServiceStub(self.channel)
    
    def close(self):
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None
    
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
    
    def _profileSerializer(self, profile):
        return {
            'id': profile.id,
            'accountID': profile.accountID,
            'fullName': profile.fullName,
            'avatarUrl': profile.avatarUrl,
            'bio': profile.bio,
            'dateOfBirth': self._parseDatetime(profile.dateOfBirth),
            'phoneNumber': profile.phoneNumber,
            'createdAt': self._parseDatetime(profile.createdAt),
            'updatedAt': self._parseDatetime(profile.updatedAt),
            'deletedAt': self._parseDatetime(profile.deletedAt),
            'isActive': profile.isActive
        }
    
    def findById(self, id):
        request = usersService_pb2.GetProfileByIDRequest(id=id)
        try:
            response = self.stub.findByID(request)
            return self._profileSerializer(response)
        except grpc.RpcError as e:
            statusCode = e.code()
            details = e.details()
            raise Exception(f"gRPC error: {statusCode} - {details}")
    
    def findByAccountID(self, accountID):
        request = usersService_pb2.GetProfileByAccountIDRequest(accountID=accountID)
        try:
            response = self.stub.findByAccountID(request)
            return self._profileSerializer(response), None
        except grpc.RpcError as e:
            statusCode = e.code()
            details = e.details()
            raise Exception(f"gRPC error: {statusCode} - {details}")
    
    def doCreate(self, accountID, fullName, avatarUrl=None, bio=None, dateOfBirth=None, phoneNumber=None):
        dobTimestamp = self._parseTimestamp(dateOfBirth) if dateOfBirth else None
        request = usersService_pb2.CreateProfileRequest(
            accountID=accountID,
            fullName=fullName,
            avatarUrl=avatarUrl or "",
            bio=bio or "",
            dateOfBirth=dobTimestamp,
            phoneNumber=phoneNumber or ""
        )
        
        try:
            response = self.stub.doCreate(request)
            return self._profileSerializer(response), None
        except grpc.RpcError as e:
            return None, ErrorCodes.OPERATION_FAILED
    
    def doUpdate(self, id, fullName=None, avatarUrl=None, bio=None, dateOfBirth=None, phoneNumber=None):
        dobTimestamp = self._parseTimestamp(dateOfBirth) if dateOfBirth else None
        
        request = usersService_pb2.UpdateProfileRequest(
            id=id,
            fullName=fullName or "",
            avatarUrl=avatarUrl or "",
            bio=bio or "",
            dateOfBirth=dobTimestamp,
            phoneNumber=phoneNumber or ""
        )
        
        try:
            response = self.stub.doUpdate(request)
            return self._profileSerializer(response)
        except grpc.RpcError as e:
            statusCode = e.code()
            details = e.details()
            raise Exception(f"gRPC error: {statusCode} - {details}")
    
    def doDelete(self, id):
        request = usersService_pb2.DeleteProfileRequest(id=id)
        try:
            response = self.stub.doDelete(request)
            return self._profileSerializer(response)
        except grpc.RpcError as e:
            statusCode = e.code()
            details = e.details()
            raise Exception(f"gRPC error: {statusCode} - {details}")