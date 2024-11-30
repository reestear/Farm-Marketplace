from django_filters import rest_framework as filters

from .models import FarmProduct


class FarmProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    min_quantity = filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    max_quantity = filters.NumberFilter(field_name="quantity", lookup_expr="lte")
    location = filters.CharFilter(field_name="farm__location", lookup_expr="icontains")

    class Meta:
        model = FarmProduct
        fields = ["min_price", "max_price", "min_quantity", "max_quantity", "location"]
