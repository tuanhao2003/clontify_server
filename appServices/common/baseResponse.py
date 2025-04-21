from django.http import JsonResponse


class BaseResponse:
    @staticmethod
    def success(message="Thành công", data=None):
        return JsonResponse(
            {
                "success": True,
                "message": message,
                "data": data,
            },
            status=200,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )

    @staticmethod
    def created(message="Tạo thành công", data=None):
        return JsonResponse(
            {
                "success": True,
                "message": message,
                "data": data,
            },
            status=201,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
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
            json_dumps_params={'ensure_ascii': False}
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
            json_dumps_params={'ensure_ascii': False}
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
            json_dumps_params={'ensure_ascii': False}
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
            json_dumps_params={'ensure_ascii': False}
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
            json_dumps_params={'ensure_ascii': False}
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
            json_dumps_params={'ensure_ascii': False}
        )
