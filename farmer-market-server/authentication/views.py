from allauth.account.utils import complete_signup
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import PasswordResetView, UserDetailsView
from django.conf import settings
from django.db import transaction
from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import FarmerStatus, UserType


class DeleteProfileImageView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = request.user  # Get the current authenticated user
        if user.image:
            user.image.delete()  # Delete the image file from storage
            user.image = None  # Set the image field to None
            user.save()  # Save the user instance to update the image field

            return Response(
                {"detail": "Profile image deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"detail": "No profile image to delete."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomUserDetailsView(UserDetailsView):
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "phone_number": {"type": "string"},
                    "user_type": {
                        "type": "string",
                        "enum": ["Administrator", "Buyer", "Farmer"],
                    },
                    "password1": {"type": "string", "format": "password"},
                    "password2": {"type": "string", "format": "password"},
                    "image": {
                        "type": "string",
                        "format": "binary",
                        "description": "The profile image to upload.",
                    },
                },
                "required": [
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "user_type",
                ],
            }
        }
    )
    def put(self, request, *args, **kwargs):
        # Handle PUT request to update user details
        return super().put(request, *args, **kwargs)

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "phone_number": {"type": "string"},
                    "image": {
                        "type": "string",
                        "format": "binary",
                        "description": "The profile image to upload.",
                    },
                },
                "required": [],
            }
        }
    )
    def patch(self, request, *args, **kwargs):
        # Handle PATCH request to update user details
        return super().patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save the updated user details
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomPasswordResetView(PasswordResetView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class CustomRegisterView(RegisterView):
    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "format": "email"},
                    "first_name": {"type": "string"},
                    "last_name": {"type": "string"},
                    "phone_number": {"type": "string"},
                    "user_type": {
                        "type": "string",
                        "enum": ["Administrator", "Buyer", "Farmer"],
                    },
                    "password1": {"type": "string", "format": "password"},
                    "password2": {"type": "string", "format": "password"},
                    "image": {
                        "type": "string",
                        "format": "binary",
                        "description": "The profile image to upload.",
                    },
                },
                "required": [
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "user_type",
                    "password1",
                    "password2",
                ],
            }
        },
        description="User registration with image upload",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                user = serializer.save(self.request)

                complete_signup(self.request, user, None, None)

                if user.user_type == UserType.FARMER:
                    user.farmer_status = FarmerStatus.PENDING
                    user.save(update_fields=["farmer_status"])
                else:
                    user.farmer_status = None
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
