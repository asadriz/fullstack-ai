from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class CookieJWTAuthentication(BaseAuthentication):
    """
    Custom authentication class that retrieves JWT from cookies.
    """

    def authenticate(self, request):
        jwt_token = request.COOKIES.get("jwt")  # Extract token from cookies
        if not jwt_token:
            return None  # No token, so authentication fails silently

        try:
            access_token = AccessToken(jwt_token)  # Decode token
            user = User.objects.get(id=access_token["user_id"])  # Get user
        except Exception as e:
            raise AuthenticationFailed("Invalid or expired token") from e

        return (user, None)  # DRF expects a tuple of (user, auth)
