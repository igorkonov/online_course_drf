from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return False
        if request.user.has_perms(
                ('course_app.view_course',
                 'course_app.change_course',
                 'course_app.view_lesson',
                 'course_app.change_lesson'
                 ),
        ):
            return True


class IsOwner(permissions.BasePermission):
    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        if request.user.pk == obj.author:
            return True
        return False
