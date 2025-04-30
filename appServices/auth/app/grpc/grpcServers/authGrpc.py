import grpc
from concurrent import futures
import time
import uuid
from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from app.grpc.protos import authService_pb2, authService_pb2_grpc
from app.services.accountsService import AccountsService
from app.services.authService import AuthService
from app.serializers.accountSerializer import AccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from common.errorCodes import ErrorCodes
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthGrpc(authService_pb2_grpc.AuthServiceServicer):
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

    def findByID(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            account, error = AccountsService.findById(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return authService_pb2.AccountResponse(
                id=str(account.id),
                roleId=str(account.roleId),
                username=account.username,
                email=account.email,
                isActive=account.isActive,
                createdAt=Timestamp(seconds=int(account.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(account.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(account.deletedAt.timestamp())) if account.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByUsername(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            account, error = AccountsService.findByUsername(request.username)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid username")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return authService_pb2.AccountResponse(
                id=str(account.id),
                roleId=str(account.roleId),
                username=account.username,
                email=account.email,
                isActive=account.isActive,
                createdAt=Timestamp(seconds=int(account.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(account.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(account.deletedAt.timestamp())) if account.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByEmail(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            account, error = AccountsService.findByEmail(request.email)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid email")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return authService_pb2.AccountResponse(
                id=str(account.id),
                roleId=str(account.roleId),
                username=account.username,
                email=account.email,
                isActive=account.isActive,
                createdAt=Timestamp(seconds=int(account.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(account.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(account.deletedAt.timestamp())) if account.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByStatus(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            accounts, error = AccountsService.findByStatus(request.isActive)
            if error == ErrorCodes.INVALID_STATUS:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid status")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No accounts found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = authService_pb2.AccountListResponse(
                totalCount=len(accounts),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for acc in accounts:
                account = response.accounts.add()
                account.id = str(acc.id)
                account.roleId = str(acc.roleId)
                account.username = acc.username
                account.email = acc.email
                account.isActive = acc.isActive
                account.createdAt = Timestamp(seconds=int(acc.createdAt.timestamp()))
                account.updatedAt = Timestamp(seconds=int(acc.updatedAt.timestamp()))
                account.deletedAt = Timestamp(seconds=int(acc.deletedAt.timestamp())) if acc.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def findByDateCreated(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            start = datetime.fromtimestamp(request.start.seconds)
            end = datetime.fromtimestamp(request.end.seconds)
            accounts, error = AccountsService.findByDateCreated(start, end)
            
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid date range")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("No accounts found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            response = authService_pb2.AccountListResponse(
                totalCount=len(accounts),
                page=request.pagination.page,
                pageSize=request.pagination.pageSize
            )
            
            for acc in accounts:
                account = response.accounts.add()
                account.id = str(acc.id)
                account.roleId = str(acc.roleId)
                account.username = acc.username
                account.email = acc.email
                account.isActive = acc.isActive
                account.createdAt = Timestamp(seconds=int(acc.createdAt.timestamp()))
                account.updatedAt = Timestamp(seconds=int(acc.updatedAt.timestamp()))
                account.deletedAt = Timestamp(seconds=int(acc.deletedAt.timestamp())) if acc.deletedAt else None
            
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def doCreate(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            account, error = AccountsService.doCreate(
                username=request.username,
                email=request.email,
                password=request.password,
                roleId=request.roleId
            )
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Username or email already exists")
                return None
            if error == ErrorCodes.CREATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create account")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return authService_pb2.AccountResponse(
                id=str(account.id),
                roleId=str(account.roleId),
                username=account.username,
                email=account.email,
                isActive=account.isActive,
                createdAt=Timestamp(seconds=int(account.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(account.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(account.deletedAt.timestamp())) if account.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def doUpdate(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            account, error = AccountsService.doUpdate(AccountSerializer.deserialize({
                "id": request.id,
                "roleId": request.roleId,
                "email": request.email,
                "password": request.password,
                "isActive": request.isActive
            }))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid input data")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Email already exists")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to update account")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return authService_pb2.AccountResponse(
                id=str(account.id),
                roleId=str(account.roleId),
                username=account.username,
                email=account.email,
                isActive=account.isActive,
                createdAt=Timestamp(seconds=int(account.createdAt.timestamp())),
                updatedAt=Timestamp(seconds=int(account.updatedAt.timestamp())),
                deletedAt=Timestamp(seconds=int(account.deletedAt.timestamp())) if account.deletedAt else None
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def doDelete(self, request, context):
        user = self._authenticate(context)
        if not user:
            return None
        try:
            result, error = AccountsService.doDelete(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Invalid ID")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to delete account")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return authService_pb2.DeleteAccountResponse(
                success=True,
                message="Account deleted successfully"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return authService_pb2.DeleteAccountResponse(success=False, message=str(e))

    def login(self, request, context):
        try:
            result, error = AuthService.login(request.username, None, request.password)
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return None
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details("Invalid password")
                return None
            if error == ErrorCodes.OPERATION_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            account, tokens, _ = result
            expires_at = datetime.now() + timedelta(minutes=30)

            return authService_pb2.LoginResponse(
                accessToken=tokens["access"],
                refreshToken=tokens["refresh"],
                expiresAt=Timestamp(seconds=int(expires_at.timestamp())),
                account=authService_pb2.AccountResponse(
                    id=str(account.id),
                    roleId=str(account.roleId),
                    username=account.username,
                    email=account.email,
                    isActive=account.isActive,
                    createdAt=Timestamp(seconds=int(account.createdAt.timestamp())),
                    updatedAt=Timestamp(seconds=int(account.updatedAt.timestamp())),
                    deletedAt=Timestamp(seconds=int(account.deletedAt.timestamp())) if account.deletedAt else None
                )
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def refreshToken(self, request, context):
        try:
            tokens, error = AuthService.refreshToken(request.refreshToken)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details("Invalid refresh token")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return None
            if error == ErrorCodes.OPERATION_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to create tokens")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            expires_at = datetime.now() + timedelta(minutes=30)

            return authService_pb2.RefreshTokenResponse(
                accessToken=tokens["access"],
                refreshToken=tokens["refresh"],
                expiresAt=Timestamp(seconds=int(expires_at.timestamp()))
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def validateToken(self, request, context):
        try:
            refresh = RefreshToken(request.accessToken)
            accountId = refresh.payload.get('id')
            
            account, error = AccountsService.findById(accountId)
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Account not found")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error")
                return None

            return authService_pb2.ValidateTokenResponse(
                isValid=True,
                account=authService_pb2.AccountResponse(
                    id=str(account.id),
                    roleId=str(account.roleId),
                    username=account.username,
                    email=account.email,
                    isActive=account.isActive,
                    createdAt=Timestamp(seconds=int(account.createdAt.timestamp())),
                    updatedAt=Timestamp(seconds=int(account.updatedAt.timestamp())),
                    deletedAt=Timestamp(seconds=int(account.deletedAt.timestamp())) if account.deletedAt else None
                )
            )
        except TokenError:
            return authService_pb2.ValidateTokenResponse(isValid=False)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    authService_pb2_grpc.add_AuthServiceServicer_to_server(AuthGrpc(), server)
    server.add_insecure_port("[::]:50050")
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
