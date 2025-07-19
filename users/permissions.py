from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.groups.filter(name='Модераторы').exists()
        )


class IsOwner(BasePermission):
    """
    Доступ разрешён только владельцу объекта.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user