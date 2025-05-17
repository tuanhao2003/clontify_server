from django.conf import settings
from common.baseResponse import BaseResponse
from common.errorCodes import ErrorCodes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class RoleMiddleware:
    def __init__(self, getResponse):
        self.getResponse = getResponse
        self.publicEndpoints = getattr(settings, 'PUBLIC_ENDPOINTS', [])
        self.accessibility = getattr(settings, 'ACCESSIBILITY', {})

    def __call__(self, request):
        if any(request.path.startswith(endpoint) for endpoint in self.publicEndpoints):
            return self.getResponse(request)

        currentPath = request.path
        endpointFound = False

        for roleKey, endpoints in self.accessibility.items():
            if any(currentPath.startswith(endpoint) for endpoint in endpoints):
                endpointFound = True
                authHeader = request.headers.get('Authorization')
                if not authHeader or not authHeader.startswith('Bearer '):
                    return BaseResponse.unauthorized(
                        "Thiếu token",
                        None,
                        ErrorCodes.UNAUTHORIZED
                    )

                try:
                    token = authHeader.split(' ')[1]
                    decodedToken = AccessToken(token)
                    userRole = decodedToken.get('role')
                    
                    if not userRole:
                        return BaseResponse.unauthorized(
                            "Token không chứa thông tin role",
                            None,
                            ErrorCodes.UNAUTHORIZED
                        )

                    requiredRole = roleKey.replace('_REQUIRED', '')
                    if userRole != requiredRole:
                        return BaseResponse.forbidden(
                            "Không có quyền truy cập",
                            None,
                            ErrorCodes.FORBIDDEN
                        )
                    
                    return self.getResponse(request)

                except (TokenError, InvalidToken) as e:
                    return BaseResponse.unauthorized(
                        "Token không hợp lệ",
                        str(e)
                    )

        if not endpointFound:
            return self.getResponse(request)

        return self.getResponse(request)
