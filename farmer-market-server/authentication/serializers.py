from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import (
    JWTSerializer,
    LoginSerializer,
    UserDetailsSerializer,
)
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import FarmerStatus, User, UserType


class CustomJWTSerializer(JWTSerializer):
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)

        # Add custom claims
        token["email"] = user.email
        token["user_type"] = user.user_type

        return token


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "id",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "phone_number",
            "is_active",
            "farmer_status",
            "image",
        )

        read_only_fields = UserDetailsSerializer.Meta.read_only_fields + (
            "id",
            "email",
            "user_type",
            "is_active",
            "farmer_status",
        )

        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "phone_number": {"required": False},
            "image": {"required": False},
        }

    def update(self, instance, validated_data):
        # Handle image update logic
        image = validated_data.get("image", None)

        if image:
            # If new image is provided, delete the old one
            if instance.image:
                instance.image.delete(save=False)
            instance.image = image  # Set the new image

        # Handle other fields like first_name, last_name, etc.
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )

        instance.save()  # Save the updated instance
        return instance

    def to_representation(self, instance):
        return super().to_representation(instance)


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    user_type = serializers.ChoiceField(
        choices=[
            (UserType.ADMINISTRATOR, "Administrator"),
            (UserType.BUYER, "Buyer"),
            (UserType.FARMER, "Farmer"),
        ],
        required=True,
    )
    image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "password",
            "image",
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
            "image": self.validated_data.get("image", ""),
        }

    def save(self, request):
        user = User(
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            phone_number=self.cleaned_data["phone_number"],
            user_type=self.cleaned_data["user_type"],
            image=self.cleaned_data["image"],
            farmer_status=(
                FarmerStatus.PENDING
                if self.cleaned_data["user_type"] == UserType.FARMER
                else None
            ),
        )
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user
