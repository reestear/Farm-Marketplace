from rest_framework import serializers

from .models import User


class FarmerRejectionSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=5000)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "user_type",
            "password",
            "farmer_status",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.is_active = False
        user.save()
        return user
