from django.contrib.auth import get_user_model

# 이메일 유효성 검사 함수

from rest_framework import serializers

from rest_framework_simplejwt.tokens import AccessToken

from .error import SIGNIN_SERIALIZE_ERRORS


# 커스텀 정의 user model 가져옴
User = get_user_model()


class SigninSerializer(serializers.Serializer):

    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    access_token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = User.objects.find_user_with_email(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                SIGNIN_SERIALIZE_ERRORS["email"]["not_found"]
            )

        if user.deleted_at:
            raise serializers.ValidationError(
                SIGNIN_SERIALIZE_ERRORS["email"]["not_found"]
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                SIGNIN_SERIALIZE_ERRORS["password"]["match"]
            )

        access_token = str(AccessToken.for_user(user))

        # 유효성 검사가 성공하면 user 객체를 반환
        return {"user": user, "access_token": access_token}
