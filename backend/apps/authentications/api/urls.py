from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from apps.authentications.api.views import (
    ChangePasswordAPI,
    LoginAPIView,
    RefreshTokenAPIView,
    ResetPasswordAPI,
    SignUpAPIView,
)

urlpatterns = [
    path("token/", LoginAPIView.as_view(), name="login_api"),
    path("token/refresh/", RefreshTokenAPIView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("reset-password/", ResetPasswordAPI.as_view()),
    path("signup/", SignUpAPIView.as_view(), name="signup_api"),
    path("change-password/", ChangePasswordAPI.as_view(), name="change_password"),
]
