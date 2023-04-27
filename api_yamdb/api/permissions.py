from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    message = 'Данное действие может выполнять только админ!'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == "admin"

    def has_permission(request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.role == "admin":
            return True
        return False
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin
