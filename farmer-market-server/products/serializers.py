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
        ]
        read_only_fields = ["id"]


# class ProductUploadPhotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "image_url",
#         ]
#         read_only_fields = ["id"]
