from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from accountsService import AccountsService
from app.serializers.accountSerializer import AccountSerializer
from common.baseResponse import BaseResponse

class AuthService:
    @staticmethod
    def login(data: dict):
        try:
            email = data.get("email")
            username = data.get("username")
            password = data.get("password")

            if not password:
                return BaseResponse.badRequest("Mật khẩu không được để trống")
            if not email and not username:
                return BaseResponse.badRequest("Tên đăng nhập hoặc email không được để trống")

            if email:
                account = AccountsService.findByEmail(email)
            else:
                account = AccountsService.findByUsername(username)

            if not account:
                return BaseResponse.notFound("Tài khoản chưa được đăng ký")
            
            if not check_password(password, account.password):
                return BaseResponse.unauthorized("Tài khoản hoặc mật khẩu không đúng")

            tokens = AuthService.createToken(account)
            accountToJSON = AccountSerializer(account).data

            return BaseResponse.success("Đăng nhập thành công", {
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
                "account": accountToJSON
            })
        except Exception as e:
            return BaseResponse.internalError("Lỗi trong quá trình đăng nhập", {"error": str(e)})

    @staticmethod
    def createToken(account):
        refresh = RefreshToken.for_user(account)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
