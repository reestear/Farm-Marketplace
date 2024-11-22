from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminApproveFarmerView,
    AdminRejectFarmerView,
    AdminStatisticsView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "users/admin/statistics", AdminStatisticsView.as_view(), name="admin_statistics"
    ),
    path(
        "users/admin/farmer/approve/<id>",
        AdminApproveFarmerView.as_view(),
        name="admin_approve_farmer",
    ),
    path(
        "users/admin/farmer/reject/<id>",
        AdminRejectFarmerView.as_view(),
        name="admin_reject_farmer",
    ),
]
