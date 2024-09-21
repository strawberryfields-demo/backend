import os
from rest_framework import serializers

from api.serializers.error import S3_URL_SERIALIZE_ERRORS
from api.utils.aws import S3


class S3URLSerializer(serializers.Serializer):
    music_metadatas = serializers.ListField(
        # DictField에 대한 구체적 확장 필요
        write_only=True,
        child=serializers.DictField(child=serializers.CharField()),
    )
    s3_urls = serializers.ListField(read_only=True, child=serializers.CharField())

    def validate(self, attrs):
        music_metadatas = attrs.get("music_metadatas")

        for music_metadata in music_metadatas:
            if not music_metadata.get("size"):
                raise serializers.ValidationError(
                    S3_URL_SERIALIZE_ERRORS["file"]["over_size"]
                )

        s3_urls = []

        s3 = S3(os.environ.get("AWS_BUCKET_NAME"))
        for music_metadata in music_metadatas:
            s3_urls.append(
                s3.generate_presigned_url(
                    object_name=f"{music_metadata['name']}.{music_metadata['extension']}",
                )
            )

        return {"s3_urls": s3_urls}
