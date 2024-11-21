from rest_framework.permissions import BasePermission
from users.models import UserType


class IsAdministrator(BasePermission):
    """
    Allows access only to users of type 'Administrator'.
    """

    def has_permission(self, request, view):

        return request.user.is_authenticated and (
            request.user.user_type == UserType.ADMINISTRATOR
            or request.user.user_type == UserType.SUPERUSER
        )
