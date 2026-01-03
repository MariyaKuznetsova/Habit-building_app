from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Класс для владельцев"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
