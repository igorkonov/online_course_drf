from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        if request.user.is_staff:
            if view.action in ['list', 'retrieve', 'update', 'partial_update']:
                return True
        return False


class IsOwner(permissions.BasePermission):
    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            if view.action in ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']:
                return True
        return False
