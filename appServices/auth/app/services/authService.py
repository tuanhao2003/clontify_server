from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from app.services.accountsService import AccountsService

class AuthService:
    @staticmethod
    def login(username, email, password):
        try:
            if email:
                account = AccountsService.findByEmail(email)
            else:
                account = AccountsService.findByUsername(username)

            if not account:
                return -1

            # if not check_password(password, account.password):
            if not (password == account.password):
                return None

            tokens = AuthService.createToken(account)
            return account, tokens
        except Exception as e:
            return None

    @staticmethod
    def createToken(account):
        refresh = RefreshToken.for_user(account)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
