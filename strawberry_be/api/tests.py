from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError


from api.serializers.error import USER_SERIALIZE_ERRORS
from .serializers import UserSerializer


# Create your tests here.
class UserManagerTests(TestCase):

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        user = self.User.objects.create_user(
            email="test@example.com",
            username="testuser",
            phone="+821012345678",
            password="password123",
            user_type="Composer",
        )
        print(f"생성된 유저: {user}")

        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("password123"))

    def test_password_hashing(self):
        user = self.User.objects.create_user(
            email="test@example.com",
            username="testuser",
            phone="+821012345678",
            password="password123",
            user_type="Composer",
        )
        self.assertNotEqual("password123", user.password)


class UserSerializerTest(TestCase):

    def setUp(self):
        # 테스트용 사용자 생성
        User = get_user_model()

        self.existing_user = User.objects.create_user(
            username="existinguser",
            phone="+821012345678",
            email="existing@example.com",
            password="existingpassword",
            user_type="Composer",
        )

    # 중복 이메일로 인한 유효성 검사 실패 테스트
    def test_email_unique_validation(self):
        data = {
            "username": "newuser",
            "phone": "+821012345678",
            "email": "existing@example.com",
            "password": "newpassword",
            "user_type": "Composer",
        }
        serializer = UserSerializer(data=data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertIn("email", context.exception.detail)
        self.assertEqual(
            context.exception.detail["email"],
            USER_SERIALIZE_ERRORS["email"]["unique"],
        )

    # 불충분한 비밀번호로 인한 사용자 생성 테스트
    def test_password_invalidation(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "phone": "+821012345678",
            "password": "password",
            "user_type": "Composer",
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    # 유효한 데이터로 인한 사용자 생성 테스트
    def test_user_creation(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "phone": "+821012345678",
            "password": "adfdqererad!",
            "user_type": "Composer",
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(user.username, data["username"])
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(user.user_type, data["user_type"])


from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserViewTests(APITestCase):
    # 회원가입 성공 API 테스트
    def test_sign_up_success(self):

        url = reverse("user-sign-up")

        data = {
            "username": "testuser",
            "phone": "+821012345678",
            "password": "testpassword123",
            "email": "testuser@example.com",
            "user_type": "Composer",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["email"], data["email"])

    # 회원가입 실패
    def test_sign_up_fail(self):

        url = reverse("user-sign-up")

        data = {
            "username": "testuser",
            "phone": "+821012345678",
            "password": "testpassword123",
            "email": "testuser@example.com",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
