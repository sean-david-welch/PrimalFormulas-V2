from rest_framework import permissions
from rest_framework.request import Request


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        is_superuser = getattr(request.user, "is_superuser", False)

        return is_superuser
