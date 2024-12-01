from django_filters import rest_framework as filters

from .models import Farm, FarmProduct


class FarmFilter(filters.FilterSet):
    farmer_id = filters.UUIDFilter(field_name="farmer__id", lookup_expr="exact")

    class Meta:
        model = Farm
        fields = ["farmer_id"]


class FarmProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_quantity = filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    max_quantity = filters.NumberFilter(field_name="quantity", lookup_expr="lte")
    location = filters.CharFilter(field_name="farm__location", lookup_expr="icontains")
    farm_id = filters.UUIDFilter(field_name="farm__id", lookup_expr="exact")
    product_id = filters.UUIDFilter(field_name="product__id", lookup_expr="exact")

    class Meta:
        model = FarmProduct
        fields = [
            "min_price",
            "max_price",
            "min_quantity",
            "max_quantity",
            "location",
            "farm_id",
            "product_id",
        ]
