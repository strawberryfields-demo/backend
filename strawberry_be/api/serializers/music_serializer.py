# JSON <-> Python 객체 변환 도움

from rest_framework import serializers
from ..models import Music


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ["id", "title", "file_path"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
