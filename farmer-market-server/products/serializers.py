from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "unit_type",
            "category",
            "image",
        ]
        read_only_fields = ["id", "image"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["image"]
