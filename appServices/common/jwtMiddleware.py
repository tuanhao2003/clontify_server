from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from common.baseResponse import BaseResponse

class JwtMiddleware:
    def __init__(self, response):
        self.response = response
        self.publicEndpoint = getattr(settings, 'PUBLIC_ENDPOINTS', [])

    def __call__(self, request):
        if any(request.path.startswith(path) for path in self.publicEndpoint):
            return self.response(request)

        requestHeader = request.headers.get("Authorization")
        if not requestHeader or not requestHeader.startswith("Bearer "):
            return BaseResponse.unauthorized("Thiếu token", None)

        accessTokenSplit = requestHeader.split(" ")[1]
        try:
            token = AccessToken(accessTokenSplit)
            request.user_id = token.get("user_id")
        except (TokenError, InvalidToken):
            return BaseResponse.unauthorized("Token không hợp lệ")

        return self.response(request)
