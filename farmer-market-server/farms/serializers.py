from farms.models import Farm, FarmProduct, FarmProductImage
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer


class FarmProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmProductImage
        fields = "__all__"
        read_only_fields = ["id", "uploaded_at", "farm_product"]


class FarmProductSerializer(serializers.ModelSerializer):
    images = FarmProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = FarmProduct
        fields = "__all__"

        read_only_fields = ["id", "image"]


class FarmSerializer(serializers.ModelSerializer):
    farmer = UserSerializer(read_only=True)
    farmer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="farmer", write_only=True
    )

    class Meta:
        model = Farm
        fields = [
            "id",
            "farmer",
            "products",
            "name",
            "size",
            "location",
            "resources",
            "farmer_id",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        print("validated_data: ", validated_data)
        return Farm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.size = validated_data.get("size", instance.size)
        instance.location = validated_data.get("location", instance.location)
        instance.resources = validated_data.get("resources", instance.resources)

        if "farmer" in validated_data:
            instance.farmer = validated_data.get("farmer", instance.farmer)

        instance.save()
        return instance
