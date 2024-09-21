from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models.music import Music
from api.serializers import MusicSerializer
from api.utils.permissions.permission import IsComposer


class MusicListView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]  # 인증 무필요 시 사용

    @action(
        detail=False, methods=["GET"], url_path="list", permission_classes=[IsComposer]
    )
    def list_music(self, request, username):

        queryset = Music.objects.filter(username__username=username)
        serializer = MusicSerializer(queryset, many=True)
        return Response(serializer.data)
