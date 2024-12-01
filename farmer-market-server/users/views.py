from core.permissions import IsAdministrator
from core.utils.response_utils import ErrorResponse, SuccessResponse
from django.conf import settings
from django.core.mail import send_mail
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .models import FarmerStatus, User, UserType
from .serializers import FarmerRejectionSerializer, UserSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Users",
        description="List all users",
        responses={200: UserSerializer(many=True)},
        parameters=[
            OpenApiParameter(
                name="user_type",
                type=OpenApiTypes.STR,
                description="Filter by user type [Farmer, Buyer, Administrator]",
            ),
            OpenApiParameter(
                name="farmer_status",
                type=OpenApiTypes.STR,
                description="Filter by farmer status [Pending, Approved, Rejected] (requires user_type=Farmer)",
            ),
        ],
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

    def get_queryset(self):
        queryset = User.objects.all()
        user_type = self.request.query_params.get("user_type")
        farmer_status = self.request.query_params.get("farmer_status")

        if user_type:
            if user_type not in [choice[0] for choice in UserType.choices]:
                raise ValidationError("Invalid user_type.")
            queryset = queryset.filter(user_type=user_type)

            if user_type == UserType.FARMER and farmer_status:
                if farmer_status not in [choice[0] for choice in FarmerStatus.choices]:
                    raise ValidationError("Invalid farmer_status.")
                queryset = queryset.filter(farmer_status=farmer_status)

        return queryset


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


class AdminApproveFarmerView(APIView):
    permission_classes = [IsAdministrator]

    @extend_schema(
        summary="Approve Farmer",
        description="Approve a farmer",
        responses={200: UserSerializer()},
    )
    def post(self, request, id):
        user = User.objects.get(id=id)

        if user.user_type != UserType.FARMER:
            return ErrorResponse({"error": "Only farmers can be approved"})

        user.farmer_status = FarmerStatus.APPROVED
        user.save(update_fields=["farmer_status"])
        return SuccessResponse(UserSerializer(user).data)


class AdminRejectFarmerView(APIView):
    permission_classes = [IsAdministrator]

    @extend_schema(
        summary="Reject Farmer",
        description="Reject a farmer with a reason and send an email",
        request=FarmerRejectionSerializer,
        responses={200: UserSerializer()},
    )
    def post(self, request, id):
        user = User.objects.get(id=id)

        if user.user_type != UserType.FARMER:
            return SuccessResponse(
                {"error": "Only farmers can be rejected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = FarmerRejectionSerializer(data=request.data)
        if serializer.is_valid():
            reason = serializer.validated_data["reason"]

            # Update farmer status
            user.farmer_status = FarmerStatus.REJECTED
            user.save(update_fields=["farmer_status"])

            # Send rejection email
            send_mail(
                subject="Your Farmer Application Rejected",
                message=f"Dear {user.first_name},\n\nYour application has been rejected for the following reason:\n\n{reason}\n\nThank you.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            return SuccessResponse(UserSerializer(user).data, status=status.HTTP_200_OK)

        return ErrorResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
