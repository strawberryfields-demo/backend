from rest_framework_simplejwt.tokens import AccessToken


class CustomAccessToken(AccessToken):
    @classmethod
    def for_user(cls, user):

        token = super().for_user(user)
        token["user_type"] = user.user_type
        return token
