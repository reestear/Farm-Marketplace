from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FarmProductView, FarmViewSet

router = DefaultRouter()
router.register(r"farms", FarmViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("farms/<int:farm_id>/products/<int:product_id>/", FarmProductView.as_view()),
]
