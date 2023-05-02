from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    message = 'Данное действие может выполнять только админ!'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_admin

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin
                or request.method in SAFE_METHODS
                )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin and request.user.is_authenticated


class IsAdminModeratorAuthor(BasePermission):

    def has_permission(self, request, view):

        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)
    
class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_admin
                or request.user.is_superuser
                or request.user.is_staff)
        )

    # def has_object_permission(self, request, view, obj):
    #     return (
    #         obj == request.user
    #         or request.user.is_admin
    #         or request.user.is_superuser)
