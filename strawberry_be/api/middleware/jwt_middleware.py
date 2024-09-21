# your_app/middleware.py
from django.contrib.auth.models import User
from api.utils.accessToken.custom_access_token import CustomAccessToken
from rest_framework_simplejwt.exceptions import TokenError


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Authorization 헤더에서 JWT 토큰을 추출
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header:
            try:
                token = auth_header.split(" ")[1]  # 'Bearer <token>'에서 토큰 추출
                payload = CustomAccessToken.get(token)  # 토큰에서 payload 추출
                user_id = payload.get("user_id")  # 사용자 ID 가져오기
                user_type = payload.get(
                    "user_type"
                )  # 사용자 type(실질적 인가) 가져오기

                # user 정보로 치환
                request.user = {
                    "user_id": user_id,
                    "user_type": user_type,
                }
            except (TokenError, User.DoesNotExist):
                request.user = None  # 사용자 설정이 실패한 경우

        else:
            request.user = None  # Authorization 헤더가 없는 경우

        response = self.get_response(request)
        return response
