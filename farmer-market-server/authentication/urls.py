from django.urls import include, path

from .views import CustomConfirmEmailView, CustomRegisterView

urlpatterns = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view(), name="custom_register"),
    path(
        "auth/accounts/confirm-email/<key>/",
        CustomConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path("auth/accounts/", include("allauth.urls")),
]
