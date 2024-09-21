# JSON <-> Python 객체 변환 도움
from math import e
import os

from rest_framework import serializers

from api.utils.aws import S3
from ..models import Music


class MusicSerializer(serializers.ModelSerializer):
    # get_file_path 메서드를 통해 file_path를 pre-signed-url으로 반환
    file_path = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = ["id", "file_uuid", "file_type", "title", "file_path"]
        extra_kwargs = {
            "file_uuid": {"read_only": True},
            "file_type": {"read_only": True},
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def get_file_path(self, obj):
        s3 = S3(os.environ.get("AWS_BUCKET_NAME"))
        object_name = f"{self.user.id}/{obj.file_uuid}.{obj.file_type}"
        return s3.geterate_presigned_url(object_name)
