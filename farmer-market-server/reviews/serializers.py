from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "buyer",
            "farm",
            "product",
            "rating",
            "text",
        ]
        read_only_fields = ["id"]
