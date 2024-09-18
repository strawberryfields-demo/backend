from django.utils import timezone
from django.contrib.auth import get_user_model

# 비밀번호 유효성 검사 함수
from django.contrib.auth.password_validation import validate_password

from django.core.validators import EmailValidator

from rest_framework import serializers

from .error import USER_SERIALIZE_ERRORS

# 커스텀 정의 user model 가져옴
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "password", "username", "phone", "user_type")
        read_only_fields = ("id",)
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "phone": {"required": True},
            "user_type": {"write_only": True, "required": True},
        }

    email = serializers.EmailField(required=True, validators=[EmailValidator()])
    # write_only: 데이터 입력 시에만 사용, 직렬화 출력에서 제외, 비밀번호 입력 시 사용, 응답에는 포함되지 않으므로 쉽게 노출 제어 가능
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    # is_valid() 호출 시 실행되는 함수 모음 (유효성 검사)
    ## is_valid() 메서드가 호출될 때, DRF는 각 필드에 대해 해당하는 validate_<field_name> 메서드를 자동으로 찾아 호출

    ## email 유효성 검사
    ### DRF는 validate_<field_name> 형식의 메서드를 자동으로 인식
    ### 단,  Serializer에 정의된 필드의 이름과 일치해야 함
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(USER_SERIALIZE_ERRORS["email"]["unique"])
        return email

    # 유저 정보 저장 메소드
    ## 유효성 검사를 통과한 데이터를 사용하여 새로운 모델 인스턴스를 생성
    ## serializers.save() 메서드를 호출하면, create() 메서드가 호출됨
    ## validated_data: 유효성 검사를 통과한 데이터 (dict)
    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            user_type=validated_data["user_type"],
        )

        return user
