from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from app.services.accountsService import AccountsService
from app.services.rolesService import RolesService
from app.grpc.grpcClients.usersGrpcClient import UsersGrpcClient
from common.errorCodes import ErrorCodes
from rest_framework_simplejwt.exceptions import TokenError

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
                return None, ErrorCodes.INVALID_INPUT

            tokens = AuthService.createToken(account)
            return account, tokens, None
        except Exception as e:
            return None, None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def createToken(account):
        try:
            refresh = RefreshToken.for_user(account)
            return {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        except Exception:
            return None

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
        try:
            existingAccount, error = AccountsService.findByUsername(username)
            if existingAccount:
                return None, ErrorCodes.ALREADY_EXISTS

            existingAccount, error = AccountsService.findByEmail(email)
            if existingAccount:
                return None, ErrorCodes.ALREADY_EXISTS

            role, error = RolesService.findByName("NORMAL")
            if error:
                return None, error

            account, error = AccountsService.doCreate(
                username=username,
                email=email,
                password=password,
                roleId=str(role.id)
            )
            if error:
                return None, error

            tokens = AuthService.createToken(account)
            if not tokens:
                return None, ErrorCodes.OPERATION_FAILED

            usersClient = UsersGrpcClient()
            try:
                profile, error = usersClient.createProfile(
                    accountID=str(account.id),
                    fullName=fullName,
                    avatarUrl=avatarUrl,
                    bio=bio,
                    dateOfBirth=dateOfBirth,
                    phoneNumber=phoneNumber,
                    token=tokens["access"]
                )
                if error:
                    AccountsService.doDelete(account.id)
                    return None, error
            finally:
                usersClient.close()

            return {
                "account": account,
                "profile": profile,
                "tokens": tokens
            }, None

        except Exception as e:
            return None, ErrorCodes.OPERATION_FAILED