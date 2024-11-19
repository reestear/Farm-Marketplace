from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import Product
from .serializers import ProductSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Products",
        description="List all products",
        responses={200: ProductSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve Product",
        description="Retrieve a product",
        responses={200: ProductSerializer()},
    ),
    create=extend_schema(
        summary="Create Product",
        description="Create a product",
        responses={201: ProductSerializer()},
    ),
    update=extend_schema(
        summary="Update Product",
        description="Update a product",
        responses={200: ProductSerializer()},
    ),
    partial_update=extend_schema(
        summary="Partial Update Product",
        description="Partial update a product",
        responses={200: ProductSerializer()},
    ),
    destroy=extend_schema(
        summary="Delete Product",
        description="Delete a product",
        responses={204: None},
    ),
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    http_method_names = ["get", "post", "patch", "delete"]
