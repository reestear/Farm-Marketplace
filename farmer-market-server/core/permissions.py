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


class IsBuyerOrFarmer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.user_type == UserType.BUYER
            or request.user.user_type == UserType.FARMER
            or request.user.user_type == UserType.SUPERUSER
        )


class IsBuyer(BasePermission):
    """
    Allows access only to users of type 'Administrator'.
    """

    def has_permission(self, request, view):

        return request.user.is_authenticated and (
            request.user.user_type == UserType.BUYER
            or request.user.user_type == UserType.SUPERUSER
        )


class IsFarmer(BasePermission):
    """
    Allows access only to users of type 'Administrator'.
    """

    def has_permission(self, request, view):

        return request.user.is_authenticated and (
            request.user.user_type == UserType.FARMER
            or request.user.user_type == UserType.SUPERUSER
        )
