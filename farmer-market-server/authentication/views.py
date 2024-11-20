from allauth.account.utils import complete_signup
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView
from django.db import transaction
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError


class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        try:
            # Use a database transaction to ensure atomicity
            with transaction.atomic():
                # Save the user but don't commit to the database yet
                user = serializer.save(self.request)

                # Attempt to complete the signup (this sends the email confirmation)
                complete_signup(self.request, user, None, None)

                user.is_active = False
                user.save(update_fields=["is_active"])

                # If we get here, everything succeeded, commit the user
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
        return redirect("http://localhost/api/docs")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
