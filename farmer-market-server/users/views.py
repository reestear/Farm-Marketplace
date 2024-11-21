from core.permissions.admin_permissions import IsAdministrator
from core.utils.response_utils import SuccessResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import FarmerStatus, User, UserType
from .serializers import UserSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Users",
        description="List all users",
        responses={200: UserSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve User",
        description="Retrieve a user",
        responses={200: UserSerializer()},
    ),
    create=extend_schema(
        summary="Create User",
        description="Create a user",
        responses={201: UserSerializer()},
    ),
    update=extend_schema(
        summary="Update User",
        description="Update a user",
        responses={200: UserSerializer()},
    ),
    partial_update=extend_schema(
        summary="Partial Update User",
        description="Partial update a user",
        responses={200: UserSerializer()},
    ),
    destroy=extend_schema(
        summary="Delete User",
        description="Delete a user",
        responses={204: None},
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdministrator]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    http_method_names = ["get", "post", "patch", "delete"]


class AdminStatisticsView(APIView):
    permission_classes = [IsAdministrator]

    @extend_schema(
        summary="Get Admin Statistics",
        description="Get statistics for the admin dashboard",
        responses={
            200: {
                "users": 0,
                "buyers": 0,
                "farmers": 0,
                "pending_farmers": 0,
            }
        },
    )
    def get(self, request):
        return SuccessResponse(
            {
                "users": User.objects.exclude(
                    user_type__in=[UserType.ADMINISTRATOR, UserType.SUPERUSER]
                ).count(),
                "buyers": User.objects.filter(user_type=UserType.BUYER).count(),
                "farmers": User.objects.filter(user_type=UserType.FARMER).count(),
                "pending_farmers": User.objects.filter(
                    user_type=UserType.FARMER, farmer_status=FarmerStatus.PENDING
                ).count(),
            }
        )
