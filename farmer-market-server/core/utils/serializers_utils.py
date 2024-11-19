# users/serializers.py
from dj_rest_auth.registration.serializers import RegisterSerializer

# users/serializers.py (add this if you're customizing login)
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from users.models import User


class CustomLoginSerializer(LoginSerializer):
    username = None  # Remove the username field entirely
    email = serializers.EmailField(required=True)  # Use email instead

    def get_authentication_method(self):
        return "email"  # Use email for authentication


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(
        choices=[
            ("Buyer", "Buyer"),
            ("Farmer", "Farmer"),
            ("Administrator", "Administrator"),
        ],
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "password",
        ]

    @property
    def cleaned_data(self):
        return {
            "email": self.validated_data.get("email", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
            "phone_number": self.validated_data.get("phone_number", ""),
            "user_type": self.validated_data.get("user_type", ""),
            "password": self.validated_data.get("password1", ""),
        }

    def save(self, request):
        user = User(
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            phone_number=self.cleaned_data["phone_number"],
            user_type=self.cleaned_data["user_type"],
        )
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user
