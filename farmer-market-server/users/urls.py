from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdminStatisticsView, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "users/admin/statistics", AdminStatisticsView.as_view(), name="admin_statistics"
    ),
]
