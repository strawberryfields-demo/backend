from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from api.serializers.signin_serializer import SigninSerializer
from api.serializers.user_serializer import UserSerializer

from rest_framework.permissions import AllowAny


class UserView(viewsets.ViewSet):

    @action(
        detail=False,
        methods=["POST"],
        url_path="sign-up",
        authentication_classes=[],
        permission_classes=[AllowAny],
    )
    def sign_up(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=["POST"],
        url_path="sign-in",
        authentication_classes=[],
        permission_classes=[AllowAny],
    )
    def sign_in(self, request):
        signin_serializer = SigninSerializer(data=request.data)
        if signin_serializer.is_valid(raise_exception=True):
            access_token = signin_serializer.validated_data.get("access_token")
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
