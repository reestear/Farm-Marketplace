from core.utils.response_utils import ErrorResponse, SuccessResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import filters as drf_filters
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import FarmProductFilter
from .models import Farm, FarmProduct, FarmProductImage
from .serializers import (
    FarmProductImageSerializer,
    FarmProductSerializer,
    FarmSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List Farms",
        description="List all farms",
        responses={200: FarmSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve Farm",
        description="Retrieve a farm",
        responses={200: FarmSerializer()},
    ),
    create=extend_schema(
        summary="Create Farm",
        description="Create a farm",
        responses={201: FarmSerializer()},
    ),
    update=extend_schema(
        summary="Update Farm",
        description="Update a farm",
        responses={200: FarmSerializer()},
    ),
    partial_update=extend_schema(
        summary="Partial Update Farm",
        description="Partial update a farm",
        responses={200: FarmSerializer()},
    ),
    destroy=extend_schema(
        summary="Delete Farm",
        description="Delete a farm",
        responses={204: None},
    ),
)
class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    http_method_names = ["get", "post", "patch", "delete"]


@extend_schema_view(
    post=extend_schema(
        summary="Create Farm Product Image",
        description="Create a farm product image",
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "image": {
                        "type": "string",
                        "format": "binary",
                        "description": "The image file to upload.",
                    }
                },
                "required": ["image"],
            }
        },
        responses={201: FarmProductImageSerializer()},
    )
)
class FarmProductImageCreateView(generics.CreateAPIView):
    queryset = FarmProductImage.objects.all()
    serializer_class = FarmProductImageSerializer

    def perform_create(self, serializer):
        farm_product_id = self.kwargs.get("farm_product_id")
        farm_product = generics.get_object_or_404(FarmProduct, id=farm_product_id)
        serializer.save(farm_product=farm_product)


@extend_schema_view(
    delete=extend_schema(
        summary="Delete Farm Product Image",
        description="Delete a farm product image",
        responses={
            204: SuccessResponse,
            404: ErrorResponse,
        },
    )
)
class FarmProductImageDeleteView(generics.DestroyAPIView):
    queryset = FarmProductImage.objects.all()

    def delete(self, request, *args, **kwargs):
        farm_product_id = kwargs.get("farm_product_id")
        image_id = kwargs.get("image_id")
        try:
            farm_product_image = FarmProductImage.objects.get(
                id=image_id, farm_product_id=farm_product_id
            )
            farm_product_image.delete()

            return SuccessResponse(
                {"message": "Image was deleted succesfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except FarmProductImage.DoesNotExist:
            return ErrorResponse(data={"message": "Image not found."})


class FarmProductViewSet(viewsets.ViewSet):
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = FarmProductFilter
    ordering_fields = ["price", "quantity"]

    def get_queryset(self):
        return FarmProduct.objects.all()

    @extend_schema(
        summary="Create Farm Product",
        description="Create a farm product.",
        request=FarmProductSerializer,
        responses={201: FarmProductSerializer},
    )
    def create(self, request):
        serializer = FarmProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="List Farm Products",
        description="List all farm products with optional filtering by price, quantity, and location.",
        responses={200: FarmProductSerializer(many=True)},
        parameters=[
            OpenApiParameter("farm_id", OpenApiTypes.UUID, description="Farm ID"),
            OpenApiParameter("product_id", OpenApiTypes.UUID, description="Product ID"),
            OpenApiParameter(
                "min_price", OpenApiTypes.NUMBER, description="Minimum price"
            ),
            OpenApiParameter(
                "max_price", OpenApiTypes.NUMBER, description="Maximum price"
            ),
            OpenApiParameter(
                "min_quantity", OpenApiTypes.NUMBER, description="Minimum quantity"
            ),
            OpenApiParameter(
                "max_quantity", OpenApiTypes.NUMBER, description="Maximum quantity"
            ),
            OpenApiParameter("location", OpenApiTypes.STR, description="Farm location"),
        ],
    )
    def list(self, request):
        farm_products = self.filter_queryset(self.get_queryset())
        serializer = FarmProductSerializer(farm_products, many=True)
        return Response(serializer.data)

    def filter_queryset(self, queryset):
        filter_backend = DjangoFilterBackend()
        return filter_backend.filter_queryset(self.request, queryset, self)

    @extend_schema(
        summary="Retrieve Farm Product",
        description="Retrieve a farm product.",
        responses={200: FarmProductSerializer},
    )
    def retrieve(self, request, farm_id, product_id):
        farm_product = self.get_object(farm_id, product_id)
        serializer = FarmProductSerializer(farm_product)
        return Response(serializer.data)

    @extend_schema(
        summary="Update Farm Product",
        description="Update a farm product.",
        request=FarmProductSerializer,
        responses={201: FarmProductSerializer},
    )
    def partial_update(self, request, farm_id, product_id):
        farm_product = self.get_object(farm_id, product_id)
        serializer = FarmProductSerializer(
            farm_product, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete Farm Product",
        description="Delete a farm product.",
        responses={204: None},
    )
    def destroy(self, request, farm_id, product_id):
        farm_product = self.get_object(farm_id, product_id)
        farm_product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, farm_id, product_id):
        return FarmProduct.objects.get(farm_id=farm_id, product_id=product_id)

    @extend_schema(
        summary="List Farm Products by Farmer",
        description="List all farm products by a specific farmer.",
        responses={200: FarmProductSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def by_farmer(self, request, farmer_id):
        farm_products = FarmProduct.objects.filter(farm__farmer__id=farmer_id)
        serializer = FarmProductSerializer(farm_products, many=True)
        return Response(serializer.data)
