from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from app.services.accountsService import AccountsService
from app.services.rolesService import RolesService
from app.grpc.grpcClients.usersGrpcClient import UsersGrpcClient
from common.errorCodes import ErrorCodes
from rest_framework_simplejwt.exceptions import TokenError
from datetime import datetime
import logging

logger = logging.getLogger('__name__')

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
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def createToken(account):
        try:
            refresh = RefreshToken.for_user(account)
            
            # role, error = RolesService.findById(account.roleId)
            # if error:
            #     return None, ErrorCodes.OPERATION_FAILED
                
            # refresh['role'] = role.name
            
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
        except Exception:
            return None, ErrorCodes.OPERATION_FAILED

    @staticmethod
    def register(username, password, email, fullName="noname", avatarUrl=None, bio=None, dateOfBirth=None, phoneNumber=None):
        try:
            logger.info(f"Starting registration process for username: {username}, email: {email}")
            
            existingAccount, error = AccountsService.findByUsername(username)
            if existingAccount:
                logger.warning(f"Registration failed - Username already exists: {username}")
                return None, ErrorCodes.ALREADY_EXISTS

            existingAccount, error = AccountsService.findByEmail(email)
            if existingAccount:
                logger.warning(f"Registration failed - Email already exists: {email}")
                return None, ErrorCodes.ALREADY_EXISTS

            role, error = RolesService.findByName("NORMAL")
            if error:
                logger.error(f"Failed to find NORMAL role: {error}")
                return None, error

            account, error = AccountsService.doCreate(
                username=username,
                email=email,
                password=make_password(password),
                roleId=str(role.id)
            )
            if error:
                logger.error(f"Failed to create account: {error}")
                return None, error

            logger.info(f"Account created successfully with ID: {account.id}")

            tokens, error = AuthService.createToken(account)
            if error or not tokens:
                logger.error(f"Failed to create tokens for account {account.id}: {error}")
                return None, ErrorCodes.OPERATION_FAILED

            usersClient = UsersGrpcClient()
            try:
                if dateOfBirth and isinstance(dateOfBirth, str):
                    try:
                        dateOfBirth = datetime.strptime(dateOfBirth, "%Y-%m-%d")
                    except ValueError:
                        logger.error(f"Invalid date format for dateOfBirth: {dateOfBirth}")
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
                    logger.error(f"Failed to create user profile for account {account.id}: {error}")
                    AccountsService.doDelete(account.id)
                    return None, error
                
                logger.info(f"User profile created successfully for account {account.id}")
            finally:
                usersClient.close()

            logger.info(f"Registration completed successfully for username: {username}")
            return {
                "account": account,
                "profile": profile,
            }, None

        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
            return None, ErrorCodes.OPERATION_FAILED