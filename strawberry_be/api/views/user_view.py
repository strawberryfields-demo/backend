from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from api.serializers.user_serializer import UserSerializer


class UserView(viewsets.ViewSet):
    @action(
        detail=False,
        methods=["POST"],
        url_path="sign-up",
        permission_classes=[AllowAny],
    )
    def sign_up(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
