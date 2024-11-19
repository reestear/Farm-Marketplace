from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets

from .models import User
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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "email"
    lookup_url_kwarg = "email"
    http_method_names = ["get", "post", "patch", "delete"]
