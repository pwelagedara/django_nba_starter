from rest_framework import permissions

from api_services import enums


class IsSuperAdmin(permissions.BasePermission):
    """Checks if User is Super Admin"""

    def has_permission(self, request, view):
        return request.user.role == enums.RoleChoice.SUPER_ADMIN


class IsAdmin(permissions.BasePermission):
    """Checks if User is an Admin"""

    def has_permission(self, request, view):
        return request.user.role == enums.RoleChoice.ADMIN


class IsCoach(permissions.BasePermission):
    """Checks if User is a Coach"""

    def has_permission(self, request, view):
        return request.user.role == enums.RoleChoice.COACH


class IsPlayer(permissions.BasePermission):
    """Checks if User is a Player"""

    def has_permission(self, request, view):
        return request.user.role == enums.RoleChoice.PLAYER