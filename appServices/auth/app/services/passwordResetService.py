import random
import string
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from app.services.accountsService import AccountsService
from common.errorCodes import ErrorCodes
from datetime import datetime, timedelta, UTC

class PasswordResetService:
    @staticmethod
    def generateVerificationCode():
        """Tạo mã xác thực 6 chữ số"""
        return ''.join(random.choices(string.digits, k=6))

    @staticmethod
    def createResetToken(email, verification_code):
        """Tạo JWT token chứa email và mã xác thực với thời hạn 15 phút"""
        token = AccessToken()
        token['email'] = email
        token['verification_code'] = verification_code
        # Set thời hạn 15 phút
        token.set_exp(from_time=datetime.now(UTC), lifetime=settings.PASSWORD_RESET_TOKEN_LIFETIME)
        return str(token)

    @staticmethod
    def sendResetEmail(email, verification_code):
        """Gửi email chứa mã xác thực"""
        subject = 'Yêu cầu đặt lại mật khẩu'
        message = f'''
        Xin chào,

        Bạn đã yêu cầu đặt lại mật khẩu. Mã xác thực của bạn là: {verification_code}

        Mã này sẽ hết hạn sau 15 phút.

        Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.

        Trân trọng,
        Clontify Team
        '''
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return True
        except Exception:
            return False

    @staticmethod
    def requestPasswordReset(email):
        """Xử lý yêu cầu đặt lại mật khẩu"""
        # Kiểm tra email tồn tại
        account, error = AccountsService.findByEmail(email)
        if error:
            return None, error

        # Tạo mã xác thực
        verification_code = PasswordResetService.generateVerificationCode()
        
        # Tạo token
        token = PasswordResetService.createResetToken(email, verification_code)
        
        # Gửi email
        if not PasswordResetService.sendResetEmail(email, verification_code):
            return None, ErrorCodes.OPERATION_FAILED

        return {"token": token}, None

    @staticmethod
    def verifyAndResetPassword(token, verification_code, new_password):
        """Xác thực mã và đặt lại mật khẩu"""
        try:
            # Giải mã token
            access = AccessToken(token)
            email = access['email']
            stored_code = access['verification_code']
            exp_timestamp = access['exp']

            current_timestamp = int(datetime.now(UTC).timestamp())
            print("DEBUG - current_timestamp:", current_timestamp)
            print("DEBUG - exp_timestamp:", exp_timestamp)
            print("DEBUG - current_datetime:", datetime.fromtimestamp(current_timestamp, UTC))
            print("DEBUG - exp_datetime:", datetime.fromtimestamp(exp_timestamp, UTC))

            if current_timestamp > exp_timestamp:
                return None, ErrorCodes.TOKEN_EXPIRED

            if verification_code != stored_code:
                return None, ErrorCodes.INVALID_VERIFICATION_CODE

            # Cập nhật mật khẩu
            account, error = AccountsService.findByEmail(email)
            if error:
                return None, error

            account.password = new_password
            updated_account, error = AccountsService.doUpdate(account)
            if error:
                return None, error

            return updated_account, None

        except Exception:
            return None, ErrorCodes.INVALID_TOKEN 