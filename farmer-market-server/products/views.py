from core.permissions import IsAdministrator
from core.utils.response_utils import (
    ErrorResponse,
    SuccessResponse,
    create_response_schema,
)
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action

from .models import Product
from .serializers import ProductImageSerializer, ProductSerializer


class ProductImageViewSet(viewsets.ViewSet):
    # permission_classes = [IsAdministrator]
    """
    A viewset for handling product images.
    """

    @extend_schema(
        summary="Add Product Image",
        description="Upload an image for the specified product.",
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
        responses={
            200: create_response_schema(
                {
                    "type": "object",
                    "properties": {
                        "image_url": {
                            "type": "string",
                            "format": "url",
                            "example": "http://example.com/media/products/images/product_image.jpg",
                        }
                    },
                    "required": ["image_url"],
                },
                status="success",
            ),
            400: create_response_schema(
                {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "File upload failed.",
                        }
                    },
                    "required": ["message"],
                },
                status="error",
            ),
        },
    )
    @action(detail=True, methods=["post"], url_path="add-image")
    def add_image(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductImageSerializer(product, data=request.data, partial=True)

        # if product.image is not None:
        #     return ErrorResponse(
        #         {"detail": "Product already has an image."},
        #         status=status.HTTP_400_BAD_REQUEST,
        #     )

        if product.image:
            product.image.delete()
            product.image = None
            product.save()

        if serializer.is_valid():
            serializer.save()
            return SuccessResponse(serializer.data, status=status.HTTP_200_OK)
        return ErrorResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @extend_schema(
    #     summary="Update Product Image",
    #     description="Update an existing product image.",
    #     request={
    #         "multipart/form-data": {
    #             "type": "object",
    #             "properties": {
    #                 "image": {
    #                     "type": "string",
    #                     "format": "binary",
    #                     "description": "The image file to upload.",
    #                 }
    #             },
    #             "required": ["image"],
    #         }
    #     },
    #     responses={
    #         200: create_response_schema(
    #             {
    #                 "type": "object",
    #                 "properties": {
    #                     "image_url": {
    #                         "type": "string",
    #                         "format": "url",
    #                         "example": "http://example.com/media/products/images/product_image.jpg",
    #                     }
    #                 },
    #                 "required": ["image_url"],
    #             },
    #             status="success",
    #         ),
    #         400: create_response_schema(
    #             {
    #                 "type": "object",
    #                 "properties": {
    #                     "message": {
    #                         "type": "string",
    #                         "example": "File update failed.",
    #                     }
    #                 },
    #                 "required": ["message"],
    #             },
    #             status="error",
    #         ),
    #     },
    # )
    # @action(detail=True, methods=["patch"], url_path="update-image")
    # def update_image(self, request, pk=None):
    #     product = get_object_or_404(Product, pk=pk)
    #     serializer = ProductImageSerializer(product, data=request.data, partial=True)

    #     if product.image:
    #         product.image.delete()
    #         product.image = None
    #         product.save()

    #     if serializer.is_valid():
    #         serializer.save()
    #         return SuccessResponse(serializer.data, status=status.HTTP_200_OK)
    #     return ErrorResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete Product Image",
        description="Delete a product's image.",
        responses={
            200: create_response_schema(
                {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "Image deleted successfully.",
                        }
                    },
                    "required": ["message"],
                },
                status="success",
            ),
            400: create_response_schema(
                {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "example": "No image to delete.",
                        }
                    },
                    "required": ["message"],
                },
                status="error",
            ),
        },
    )
    @action(detail=True, methods=["delete"], url_path="delete-image")
    def delete_image(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)

        if product.image:
            product.image.delete()
            product.image = None
            product.save()
            return SuccessResponse(
                {"detail": "Image deleted successfully."}, status=status.HTTP_200_OK
            )
        return ErrorResponse(
            {"detail": "No image to delete."}, status=status.HTTP_400_BAD_REQUEST
        )


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
