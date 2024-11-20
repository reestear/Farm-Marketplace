from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + (
            "email",
            "first_name",
            "last_name",
            "user_type",
            "phone_number",
        )

    def to_representation(self, instance):
        print("CustomUserDetailsSerializer is being called.")
        return super().to_representation(instance)


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         user = self.user
#         data["user"] = {
#             "pk": str(user.id),
#             "email": user.email,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "user_type": user.user_type,
#         }
#         return data

#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         # Add custom claims to the token payload
#         token["first_name"] = user.first_name
#         token["last_name"] = user.last_name
#         token["user_type"] = (
#             user.user_type
#         )  # Ensure this field exists on your User model
#         return token


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
