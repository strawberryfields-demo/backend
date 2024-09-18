from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..serializers import SigninSerializer


class SigninSerializerTests(TestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.User = get_user_model()

        self.existing_user = self.User.objects.create_user(
            username="existinguser",
            phone="+821012345678",
            email="existing@example.com",
            password="existingpassword",
            user_type="Composer",
        )

    # 올바른 데이터로 로그인 성공 테스트
    def test_signin_success(self):
        data = {
            "email": "existing@example.com",
            "password": "existingpassword",
        }
        serializer = SigninSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.validated_data["user"]
        self.assertEqual(user.email, data["email"])

        # 올바른 데이터로 로그인 실패 테스트

    def test_signin_failure(self):
        data = {
            "email": "existing@example.com",
            "password": "123423425",
        }
        serializer = SigninSerializer(data=data)
        self.assertFalse(serializer.is_valid())


from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserViewTests(APITestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.User = get_user_model()

        self.existing_user = self.User.objects.create_user(
            username="existinguser",
            phone="+821012345678",
            email="testuser@example.com",
            password="testpassword123",
            user_type="Composer",
        )

    # 로그인 성공 API 테스트
    def test_signin_api_success(self):

        url = reverse("user-sign-in")

        data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], data["email"])

    # 로그인 실패
    def test_signin_api_fail(self):

        url = reverse("user-sign-in")

        data = {
            "email": "testuser@example.com",
            "password": "wrongpassword123",
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
