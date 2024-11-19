from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import Review
from .serializers import ReviewSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Reviews",
        description="List all reviews",
        responses={200: ReviewSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve Review",
        description="Retrieve a review",
        responses={200: ReviewSerializer()},
    ),
    create=extend_schema(
        summary="Create Review",
        description="Create a review",
        responses={201: ReviewSerializer()},
    ),
    update=extend_schema(
        summary="Update Review",
        description="Update a review",
        responses={200: ReviewSerializer()},
    ),
    partial_update=extend_schema(
        summary="Partial Update Review",
        description="Partial update a review",
        responses={200: ReviewSerializer()},
    ),
    destroy=extend_schema(
        summary="Delete Review",
        description="Delete a review",
        responses={204: None},
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    http_method_names = ["get", "post", "patch", "delete"]
