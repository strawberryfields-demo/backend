import os
import uuid
from rest_framework import serializers

from api.serializers.error import S3_URL_SERIALIZE_ERRORS
from api.utils.aws import S3
from api.models import user
from api.models.music import Music


class S3URLSerializer(serializers.Serializer):
    music_metadatas = serializers.ListField(
        # DictField에 대한 구체적 확장 필요
        write_only=True,
        child=serializers.DictField(child=serializers.CharField()),
    )
    s3_urls = serializers.ListField(read_only=True, child=serializers.CharField())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        music_metadatas = attrs.get("music_metadatas")

        for music_metadata in music_metadatas:
            if music_metadata.get("extension") not in ["mp3", "wav"]:
                raise serializers.ValidationError(
                    S3_URL_SERIALIZE_ERRORS["file"]["invalid_extension"]
                )
            if not music_metadata.get("size"):
                raise serializers.ValidationError(
                    S3_URL_SERIALIZE_ERRORS["file"]["over_size"]
                )

        s3_urls = []
        music_objects = []

        s3 = S3(os.environ.get("AWS_BUCKET_NAME"))
        for music_metadata in music_metadatas:
            original_filename = f"{music_metadata['name']}"
            file_uuid = uuid.uuid4()
            file_extension = f".{music_metadata['extension']}"

            object_name = f"{self.user.id}/{file_uuid}.{music_metadata['extension']}"
            s3_urls.append(
                s3.generate_presigned_post(
                    object_name=object_name,
                )
            )

            music = Music(
                user=self.user,
                file_uuid=file_uuid,
                title=music_metadata["name"],
                file_path=f"https://{s3.bucket_name}.s3.{s3.location}.amazonaws.com/{object_name}",
                file_type=music_metadata["extension"],
                status="uploaded",
            )

            music_objects.append(music)

        Music.objects.bulk_create(music_objects)
        return {"s3_urls": s3_urls}
