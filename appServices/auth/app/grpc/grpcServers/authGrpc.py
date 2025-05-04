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

class AuthGrpc(authService_pb2_grpc.AuthServiceServicer):

    def findByID(self, request, context):
        try:
            account, error = AccountsService.findById(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Tài khoản không hợp lệ")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
        try:
            account, error = AccountsService.findByUsername(request.username)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("username không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy tài khoản")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
        try:
            account, error = AccountsService.findByEmail(request.email)
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Email không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy tài khoản")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
        try:
            accounts, error = AccountsService.findByStatus(request.isActive)
            if error == ErrorCodes.INVALID_STATUS:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Trạng thái không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm được tài khoản nào")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
        try:
            start = datetime.fromtimestamp(request.start.seconds)
            end = datetime.fromtimestamp(request.end.seconds)
            accounts, error = AccountsService.findByDateCreated(start, end)
            
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Khoảng thời gian không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm được tài khoản nào")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[doCreate] Nhận yêu cầu tạo tài khoản - username: {request.username}, email: {request.email}, roleId: {request.roleId}")
        try:
            account, error = AccountsService.doCreate(
                username=request.username,
                email=request.email,
                password=request.password,
                roleId=request.roleId
            )

            if error == ErrorCodes.INVALID_INPUT:
                logger.warning(f"[doCreate] Dữ liệu không hợp lệ cho username: {request.username}")
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("Dữ liệu không hợp lệ")
                return None

            if error == ErrorCodes.ALREADY_EXISTS:
                logger.warning(f"[doCreate] Tài khoản đã tồn tại - username: {request.username}, email: {request.email}")
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Tài khoản đã tồn tại")
                return None

            if error == ErrorCodes.CREATE_FAILED:
                logger.error(f"[doCreate] Lỗi khi tạo tài khoản cho username: {request.username}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi khi tạo tài khoản")
                return None

            if error:
                logger.error(f"[doCreate] Lỗi hệ thống không xác định - username: {request.username}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None

            logger.info(f"[doCreate] Tạo tài khoản thành công - id: {account.id}, username: {account.username}")
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
            logger.exception(f"[doCreate] Exception xảy ra khi tạo tài khoản - username: {request.username}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return None

    def doUpdate(self, request, context):
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
                context.set_details("Thông tin không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy tài khoản")
                return None
            if error == ErrorCodes.ALREADY_EXISTS:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Email đã tồn tại")
                return None
            if error == ErrorCodes.UPDATE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi khi cập nhật tài khoản")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
        try:
            result, error = AccountsService.doDelete(uuid.UUID(request.id))
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details("ID không hợp lệ")
                return None
            if error == ErrorCodes.DELETE_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi khi xóa tài khoản")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None

            return authService_pb2.DeleteAccountResponse(
                success=True,
                message="Tài khoản đã được xóa"
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return authService_pb2.DeleteAccountResponse(success=False, message=str(e))

    def doLogin(self, request, context):
        try:
            result, error = AuthService.login(request.username, None, request.password)
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Tài khoản chưa đăng ký")
                return None
            if error == ErrorCodes.INVALID_INPUT:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details("Mật khẩu không chính xác")
                return None
            if error == ErrorCodes.OPERATION_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
                context.set_details("Token không hợp lệ")
                return None
            if error == ErrorCodes.NOT_FOUND:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Không tìm thấy tài khoản")
                return None
            if error == ErrorCodes.OPERATION_FAILED:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi khi cấp token")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
                context.set_details("Không tìm thấy tài khoản")
                return None
            if error:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Lỗi hệ thống")
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
