from django.http import JsonResponse

class BaseResponse:
    @staticmethod
    def success(message="Thành công", data=None):
        return JsonResponse(
            {"success": True, "message": message, "data": data},
            status=200,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def created(message="Tạo thành công", data=None):
        return JsonResponse(
            {"success": True, "message": message, "data": data},
            status=201,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def badRequest(message="Yêu cầu không hợp lệ", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=400,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def unauthorized(message="Chưa xác thực", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=401,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def paymentRequired(message="Yêu cầu thanh toán", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=402,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def forbidden(message="Không có quyền truy cập", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=403,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def notFound(message="Không tìm thấy", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=404,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def methodNotAllowed(message="Phương thức không được phép", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=405,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def conflict(message="Xung đột dữ liệu", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=409,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def alreadyExists(message="Dữ liệu đã tồn tại", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=409,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def tooManyRequests(message="Quá nhiều yêu cầu", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=429,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def internalError(message="Lỗi máy chủ", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=500,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def createFailed(message="Tạo dữ liệu thất bại", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=550,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def updateFailed(message="Cập nhật dữ liệu thất bại", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=551,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def deleteFailed(message="Xóa dữ liệu thất bại", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=552,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def tokenExpired(message="Token đã hết hạn", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=700,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
    
        )
    @staticmethod
    def invalidToken(message="Token không hợp lệ", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=701,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def insufficientPermissions(message="Không đủ quyền thực hiện", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=702,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def externalServiceError(message="Lỗi dịch vụ bên ngoài", data=None):
        return JsonResponse(
            {
                "success": False,
                "message": message,
                "data": data,
            },
            status=900,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )
