from allauth.account.utils import complete_signup
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import PasswordResetView
from django.conf import settings
from django.db import transaction
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError
from users.models import FarmerStatus, UserType


class CustomPasswordResetView(PasswordResetView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                user = serializer.save(self.request)

                complete_signup(self.request, user, None, None)

                if user.user_type == UserType.FARMER:
                    user.farmer_status = FarmerStatus.PENDING
                    user.save(update_fields=["farmer_status"])

                user.is_active = False
                user.save(update_fields=["is_active"])

                return user
        except Exception as e:
            raise ValidationError({"error": f"Registration failed: {str(e)}"})


class CustomConfirmEmailView(ConfirmEmailView):
    def post(self, request, *args, **kwargs):
        confirmation = self.get_object()
        confirmation.confirm(request)

        user = confirmation.email_address.user
        if user and not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        return redirect(settings.LOGIN_REDIRECT_URL)

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
