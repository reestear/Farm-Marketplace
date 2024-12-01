import django_filters
from orders.models import Order, OrderFarmProduct
from orders.types.order_types import OrderStatusType


class OrderFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        field_name="status", choices=OrderStatusType.choices, label="Order Status"
    )

    class Meta:
        model = Order
        fields = ["status"]


class OrderFarmProductFilter(django_filters.FilterSet):
    order_id = django_filters.UUIDFilter(field_name="order__id", lookup_expr="exact")
    farm_id = django_filters.UUIDFilter(field_name="farm__id", lookup_expr="exact")
    product_id = django_filters.UUIDFilter(
        field_name="product__id", lookup_expr="exact"
    )

    class Meta:
        model = OrderFarmProduct
        fields = ["order_id", "farm_id", "product_id"]


class CartFarmProductFilter(django_filters.FilterSet):
    farm_id = django_filters.UUIDFilter(field_name="farm__id", lookup_expr="exact")
    product_id = django_filters.UUIDFilter(
        field_name="product__id", lookup_expr="exact"
    )

    class Meta:
        model = OrderFarmProduct
        fields = ["farm_id", "product_id"]
