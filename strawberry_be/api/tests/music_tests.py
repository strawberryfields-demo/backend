from django.test import TestCase
from django.contrib.auth import get_user_model

from api.serializers.s3_url_serializer import S3URLSerializer


class MusicSerializerTests(TestCase):
    pass


from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MusicViewTests(APITestCase):
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

    # 로그인 성공/url얻기 성공 API 테스트
    def test_get_s3_url_success(self):
        login_url = reverse("user-sign-in")
        music_upload_url = reverse("music-upload")
        user_data = {
            "email": "testuser@example.com",
            "password": "testpassword123",
        }
        response = self.client.post(login_url, user_data, format="json")
        # token 얻기
        acess_token = response.data["access_token"]

        music_metadatas = {
            "music_metadatas": [
                {"name": "test", "extension": "mp3", "size": "100"},
                {"name": "test2", "extension": "mp3", "size": "100"},
                {"name": "test3", "extension": "mp3", "size": "100"},
            ]
        }
        serializers = S3URLSerializer(data=music_metadatas)
        serializers.is_valid(raise_exception=True)

        # s3 url 얻기 (인가된 사용자)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {acess_token}")
        response = self.client.post(
            music_upload_url, data=music_metadatas, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["s3_urls"]), 3)
