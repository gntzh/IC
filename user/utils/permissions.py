from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    BasePermission,
    SAFE_METHODS
)


class UserCreatePermission(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in ('POST', 'GET', 'HEAD', 'OPTIONS') or
            request.user and
            request.user.is_authenticated
        )


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return IsAuthenticated().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.user and request.user == obj:
            return bool(
                request.user == obj
            )
        else:
            return IsAdminUser().has_permission(request, view)


class SafeCreate(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        else:
            return IsAuthenticated().has_permission(request, view)


class OwnerAction(BasePermission):
    def has_object_permission(self, request, view, obj):
        owner_action = ["PUT", "PATCH"]
        if request.method in owner_action:
            return bool(request.user == obj)
        else:
            return True


class AdminAction(BasePermission):
    def has_permission(self, request, view):
        admin_action = ["GET", "DELETE"]
        if request.method in admin_action:
            return IsAdminUser().has_permission(request, view)
        return True
