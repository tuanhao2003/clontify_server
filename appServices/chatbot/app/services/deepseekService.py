from django.views import View
import requests
import os
import json
from common.baseResponse import BaseResponse


class RequestDeepseek(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            prompt = data.get("prompt")
            apiKey = os.getenv("DEEPSEEK_API_KEY")
            if not apiKey:
                return BaseResponse.externalServiceError("Apikey không hợp lệ")

            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {apiKey}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "deepseek/deepseek-chat:free",
                "messages": [{"role": "user", "content": prompt}],
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return BaseResponse.success(data=response.json())
        except Exception as e:
            return BaseResponse.internalError(data=str(e))
