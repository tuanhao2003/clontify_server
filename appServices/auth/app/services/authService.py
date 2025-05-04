from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from app.services.accountsService import AccountsService
from app.services.rolesService import RolesService
from app.grpc.grpcClients.usersGrpcClient import UsersGrpcClient
from common.errorCodes import ErrorCodes
from rest_framework_simplejwt.exceptions import TokenError
from datetime import datetime

class AuthService:
    @staticmethod
    def login(username, email, password):
        try:
            if email:
                account, error = AccountsService.findByEmail(email)
            else:
                account, error = AccountsService.findByUsername(username)

            if error:
                return None, error

            if not check_password(password, account.password):
                return None, ErrorCodes.UNAUTHORIZED

            tokens, error = AuthService.createToken(account)
            if(error):
                return None, ErrorCodes.OPERATION_FAILED
            
            return {"account": account, "tokens": tokens}, None
        except Exception as e:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def createToken(account):
        try:
            refresh = RefreshToken.for_user(account)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, None
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def refreshToken(refreshToken):
        try:
            refresh = RefreshToken(refreshToken)
            accountId = refresh.payload.get('user_id')
            
            account, error = AccountsService.findById(accountId)
            if error:
                return None, error

            tokens = AuthService.createToken(account)
            if not tokens:
                return None, ErrorCodes.OPERATION_FAILED

            return tokens, None
        except TokenError:
            return None, ErrorCodes.INVALID_INPUT
        except Exception as e:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def register(username, password, email, fullName="noname", avatarUrl=None, bio=None, dateOfBirth=None, phoneNumber=None):
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"[register] Bắt đầu đăng ký - username: {username}, email: {email}")
        try:
            existingAccount, error = AccountsService.findByUsername(username)
            if existingAccount:
                logger.warning(f"[register] Username đã tồn tại: {username}")
                return None, ErrorCodes.ALREADY_EXISTS

            existingAccount, error = AccountsService.findByEmail(email)
            if existingAccount:
                logger.warning(f"[register] Email đã tồn tại: {email}")
                return None, ErrorCodes.ALREADY_EXISTS

            role, error = RolesService.findByName("NORMAL")
            if error:
                logger.error(f"[register] Không tìm thấy role NORMAL")
                return None, error

            account, error = AccountsService.doCreate(
                username=username,
                email=email,
                password=make_password(password),
                roleId=str(role.id)
            )
            if error:
                logger.error(f"[register] Tạo tài khoản thất bại - username: {username}")
                return None, error
            logger.info(f"[register] Đã tạo account - ID: {account.id}, username: {username}")

            tokens, error = AuthService.createToken(account)
            if error or not tokens:
                logger.error(f"[register] Tạo token thất bại cho accountID: {account.id}")
                return None, ErrorCodes.OPERATION_FAILED
            logger.info(f"[register] Token tạo thành công cho accountID: {account.id}")

            usersClient = UsersGrpcClient()
            try:
                if dateOfBirth and isinstance(dateOfBirth, str):
                    try:
                        dateOfBirth = datetime.strptime(dateOfBirth, "%Y-%m-%d")
                    except ValueError:
                        logger.error(f"[register] Sai định dạng dateOfBirth - username: {username}, value: {dateOfBirth}")
                        return None, ErrorCodes.INVALID_INPUT
                    
                profile, error = usersClient.doCreate(
                    accountID=str(account.id),
                    fullName=fullName,
                    avatarUrl=avatarUrl,
                    bio=bio,
                    dateOfBirth=dateOfBirth,
                    phoneNumber=phoneNumber
                )
                if error:
                    logger.error(f"[register] Tạo profile thất bại - rollback accountID: {account.id}")
                    AccountsService.doDelete(account.id)
                    return None, error
                logger.info(f"[register] Tạo profile thành công cho accountID: {account.id}")
            finally:
                usersClient.close()
                logger.debug(f"[register] Đã đóng kết nối usersClient")

            logger.info(f"[register] Đăng ký thành công - accountID: {account.id}")
            return {
                "account": account,
                "profile": profile,
            }, None

        except Exception as e:
            logger.exception(f"[register] Lỗi không xác định - username: {username}")
            return None, ErrorCodes.OPERATION_FAILED