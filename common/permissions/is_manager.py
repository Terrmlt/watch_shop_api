from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'is_manager') and request.user.is_manager
