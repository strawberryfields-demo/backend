from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from api.models.music import Music
from api.serializers import MusicSerializer
from api.utils.permissions.permission import IsComposer
from api.serializers.s3_url_serializer import S3URLSerializer


class MusicView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(
        detail=False,
        methods=["GET"],
        url_path="list",
        permission_classes=[IsAuthenticated, IsComposer],
    )
    def list_music(self, request):
        queryset = Music.objects.filter(user=request.user).all()
        paginator = PageNumberPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = MusicSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @action(
        detail=False,
        methods=["POST"],
        url_path="upload",
        url_name="upload",
        permission_classes=[IsAuthenticated, IsComposer],
    )
    def upload_music(self, request):
        serializer = S3URLSerializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)

        s3_urls = serializer.validated_data["s3_urls"]
        return Response({"s3_urls": s3_urls}, status=status.HTTP_200_OK)
