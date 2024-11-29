from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    FarmProductImageCreateView,
    FarmProductImageDeleteView,
    FarmProductViewSet,
    FarmViewSet,
)

router = DefaultRouter()
router.register(r"farms", FarmViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "farm-products/", FarmProductViewSet.as_view({"post": "create", "get": "list"})
    ),
    path(
        "farm-products/<uuid:farm_id>/<uuid:product_id>/",
        FarmProductViewSet.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
    path(
        "farm-products/by-farmer/<uuid:farmer_id>",
        FarmProductViewSet.as_view({"get": "by_farmer"}),
    ),
    path(
        "farm-products/<int:farm_product_id>/add-image/",
        FarmProductImageCreateView.as_view(),
        name="add_farm_product_image",
    ),
    path(
        "farm-products/<int:farm_product_id>/remove-image/<int:image_id>/",
        FarmProductImageDeleteView.as_view(),
        name="remove_farm_product_image",
    ),
]
