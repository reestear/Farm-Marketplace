from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductImageViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet)

product_image_viewset = ProductImageViewSet.as_view(
    {
        "post": "add_image",
        # "patch": "update_image",
        "delete": "delete_image",
    }
)


urlpatterns = [
    path("", include(router.urls)),
    path("products/<uuid:pk>/image/", product_image_viewset, name="product-image"),
]
