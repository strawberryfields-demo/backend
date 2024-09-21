from django.test import TestCase

from api.utils.aws import S3
from api.serializers.s3_url_serializer import S3URLSerializer


class S3AwsTest(TestCase):
    def setUp(self):
        self.s3 = S3("strawberry-demo-music-bucket")

    def test_s3_bucket_name(self):
        self.assertEqual(self.s3.bucket_name, "strawberry-demo-music-bucket")


class S3SerializerTest(TestCase):
    def test_s3_urls_success(self):
        data = {
            "music_metadatas": [
                {"name": "test1", "extension": "mp3", "size": 1024},
                {"name": "test2", "extension": "mp3", "size": 1024},
            ]
        }
        serializer = S3URLSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        s3_urls = serializer.validated_data["s3_urls"]
        self.assertEqual(len(s3_urls), 2)
