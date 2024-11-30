from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import include, path

from .views import (
    CustomConfirmEmailView,
    CustomRegisterView,
    CustomUserDetailsView,
    DeleteProfileImageView,
)

urlpatterns = [
    path("auth/user/", CustomUserDetailsView.as_view(), name="custom_user_details"),
    path(
        "auth/user/delete-image/",
        DeleteProfileImageView.as_view(),
        name="delete_profile_image",
    ),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view(), name="custom_register"),
    path(
        "auth/accounts/confirm-email/<key>/",
        CustomConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("auth/accounts/", include("allauth.urls")),
    path(
        "auth/password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
