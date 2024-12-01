from core.permissions import IsBuyer, IsFarmer
from core.utils.response_utils import ErrorResponse, SuccessResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from farms.models import Farm
from orders.models import Order, OrderFarmProduct
from orders.serializers import OrderSerializer
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import CartFarmProductFilter, OrderFarmProductFilter, OrderFilter
from .serializers import (
    AddProductSerializer,
    BuyerEditProductSerializer,
    FarmerEditProductSerializer,
    OrderCreateSerializer,
    OrderFarmProductSerializer,
    PurchaseOrderSerializer,
)
from .types.order_types import OrderStatusType


class CreateOrderView(generics.GenericAPIView):
    permission_classes = [IsBuyer]
    serializer_class = OrderCreateSerializer

    def post(self, request, *args, **kwargs):
        buyer = request.user

        if Order.objects.filter(buyer=buyer, status=OrderStatusType.CART).exists():
            raise ValidationError("You already have an active cart.")

        order = Order.objects.create(buyer=buyer, status=OrderStatusType.CART)

        serializer = self.get_serializer(order)
        return SuccessResponse(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="status",
                description="Filter orders by status",
                required=False,
                type=str,
                enum=["Cart", "Ordered", "Delivered"],
            ),
        ]
    )
)
class BuyerOrderListView(generics.ListAPIView):
    """
    View to retrieve all orders for the authenticated buyer.
    """

    permission_classes = [IsBuyer]
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_queryset(self):
        """
        Return orders belonging to the authenticated buyer.
        """
        return Order.objects.filter(buyer=self.request.user)


class OrderFarmProductListView(generics.ListAPIView):
    permission_classes = [IsBuyer]

    serializer_class = OrderFarmProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFarmProductFilter

    def get_queryset(self):
        buyer_id = self.request.user.id

        return OrderFarmProduct.objects.filter(order__buyer=buyer_id)


class CartFarmProductListView(generics.ListAPIView):
    permission_classes = [IsBuyer]

    serializer_class = OrderFarmProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CartFarmProductFilter

    def get_queryset(self):
        buyer_id = self.request.user.id

        return OrderFarmProduct.objects.filter(
            order__buyer=buyer_id, order__status=OrderStatusType.CART
        )


@extend_schema(
    request=AddProductSerializer,
    responses={
        201: OpenApiResponse(description="Product added to order successfully."),
        400: OpenApiResponse(description="Invalid data or error occurred."),
        403: OpenApiResponse(description="Unauthorized action."),
    },
)
class AddProductToOrderView(APIView):
    permission_classes = [IsBuyer]

    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(
            buyer=request.user, status=OrderStatusType.CART
        ).first()

        if not order:
            return ErrorResponse(
                {"detail": "You don't have an active cart."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.buyer != request.user:
            return ErrorResponse(
                {"detail": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AddProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                print(
                    "serializer.validated_data: ", serializer.validated_data, flush=True
                )
                farm = serializer.validated_data["farm"]
                product = serializer.validated_data["product"]
                quantity = serializer.validated_data["quantity"]
                price = serializer.validated_data["price"]
                order.add_product_from_farm(farm, product, quantity, price)
                return Response(
                    {"detail": "Product added to order successfully."},
                    status=status.HTTP_201_CREATED,
                )
            except ValueError as e:
                return ErrorResponse(
                    {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )
        return SuccessResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=BuyerEditProductSerializer,
    responses={
        200: OpenApiResponse(description="Product updated successfully."),
        400: OpenApiResponse(description="Invalid data or error occurred."),
        403: OpenApiResponse(description="Unauthorized action."),
    },
)
class BuyerEditProductInOrderView(APIView):
    permission_classes = [IsBuyer]

    def patch(self, request, farm_id, product_id, *args, **kwargs):
        order = Order.objects.filter(
            buyer=request.user, status=OrderStatusType.CART
        ).first()

        if not order:
            return ErrorResponse(
                {"detail": "You don't have an active cart."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.buyer != request.user:
            return ErrorResponse(
                {"detail": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = BuyerEditProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                quantity = serializer.validated_data.get("quantity")

                order.edit_product_from_farm(
                    farm_id, product_id, quantity=quantity, price=None
                )
                return Response(
                    {"detail": "Product updated in order successfully."},
                    status=status.HTTP_200_OK,
                )
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=FarmerEditProductSerializer,
    responses={
        200: OpenApiResponse(description="Product updated successfully."),
        400: OpenApiResponse(description="Invalid data or error occurred."),
        403: OpenApiResponse(description="Unauthorized action."),
    },
)
class FarmerEditProductInOrderView(APIView):
    permission_classes = [IsFarmer]

    def patch(self, request, order_id, farm_id, product_id, *args, **kwargs):
        order = Order.objects.get(id=order_id)
        farm = Farm.objects.get(id=farm_id)

        if farm.farmer != request.user:
            return ErrorResponse(
                {
                    "detail": "You should be the farmer of the given farm to perform this action."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = FarmerEditProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                price = serializer.validated_data.get("price")

                order.edit_product_from_farm(
                    farm_id, product_id, quantity=None, price=price
                )
                return Response(
                    {"detail": "Product updated in order successfully."},
                    status=status.HTTP_200_OK,
                )
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=None,
    responses={
        204: OpenApiResponse(description="Product removed successfully."),
        400: OpenApiResponse(description="Invalid data or error occurred."),
        403: OpenApiResponse(description="Unauthorized action."),
    },
)
class RemoveProductFromOrderView(APIView):
    permission_classes = [IsBuyer]

    def delete(self, request, farm_id, product_id, *args, **kwargs):
        order = Order.objects.filter(
            buyer=request.user, status=OrderStatusType.CART
        ).first()

        if not order:
            return ErrorResponse(
                {"detail": "You don't have an active cart."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.buyer != request.user:
            return ErrorResponse(
                {"detail": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order.remove_product_from_farm(farm_id, product_id)
            return Response(
                {"detail": "Product removed from order successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=PurchaseOrderSerializer,
    responses={
        200: OpenApiResponse(description="Order purchased successfully."),
        400: OpenApiResponse(description="Invalid data or error occurred."),
        403: OpenApiResponse(description="Unauthorized action."),
    },
)
class PurchaseOrderView(APIView):
    permission_classes = [IsBuyer]

    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(
            buyer=request.user, status=OrderStatusType.CART
        ).first()

        if not order:
            return ErrorResponse(
                {"detail": "You don't have an active cart."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.buyer != request.user:
            return ErrorResponse(
                {"detail": "You are not authorized to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                payment_details = {
                    "method": serializer.validated_data["payment_method"],
                    "amount": serializer.validated_data["payment_amount"],
                }
                delivery_details = {
                    "address": serializer.validated_data["delivery_address"],
                    "delivery_date": serializer.validated_data["delivery_date"],
                }
                order.purchase(payment_details, delivery_details)
                return Response(
                    {"detail": "Order purchased successfully."},
                    status=status.HTTP_200_OK,
                )
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
