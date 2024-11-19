from core.utils.response_utils import SuccessResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from products.models import Product
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Farm, FarmProduct
from .serializers import FarmProductSerializer, FarmSerializer


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


# Add product to farm


class FarmProductView(APIView):

    @extend_schema(
        summary="Add Product to Farm",
        description="Add a product to a farm",
        request=FarmProductSerializer,  # Include serializer for input validation
        responses={
            201: FarmProductSerializer
        },  # Response can include the created object
    )
    def post(self, request, farm_id, product_id):
        serializer = FarmProductSerializer(
            data={"farm_id": farm_id, "product_id": product_id}
        )
        if serializer.is_valid():
            serializer.save()  # Save the validated data
            return SuccessResponse(
                {"message": "Successfully added Product to Farm"}, status=201
            )
        return Response(serializer.errors, status=400)

    @extend_schema(
        summary="Delete Product from Farm",
        description="Delete a product from a farm",
        responses={204: None},
    )
    def delete(self, request, farm_id, product_id):
        farm = Farm.objects.get(id=farm_id)
        product = Product.objects.get(id=product_id)
        farm_product = FarmProduct.objects.get(farm=farm, product=product)
        farm_product.delete()
        return SuccessResponse(
            {"message": "Successfully deleted Product from Farm"}, status=204
        )
