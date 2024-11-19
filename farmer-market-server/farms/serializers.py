from farms.models import Farm, FarmProduct
from products.models import Product

# farms/serializers.py
from rest_framework import serializers
from users.models import User
from users.serializers import UserSerializer


class FarmProductSerializer(serializers.Serializer):
    farm_id = serializers.PrimaryKeyRelatedField(queryset=Farm.objects.all())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    def create(self, validated_data):
        farm = validated_data.get("farm_id")
        product = validated_data.get("product_id")
        farm_product = FarmProduct.objects.create(farm=farm, product=product)
        return farm_product


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
        # farmer is already handled by the PrimaryKeyRelatedField, no need to pop or fetch manually
        print("validated_data: ", validated_data)
        return Farm.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.size = validated_data.get("size", instance.size)
        instance.location = validated_data.get("location", instance.location)
        instance.resources = validated_data.get("resources", instance.resources)

        # Farmer can be updated if passed in validated_data
        if "farmer" in validated_data:
            instance.farmer = validated_data.get("farmer", instance.farmer)

        instance.save()
        return instance
