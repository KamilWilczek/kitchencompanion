from rest_framework.permissions import BasePermission


class IsOwnerOrSharedUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True

        if request.user in obj.shared_with.all():
            return True

        return False
