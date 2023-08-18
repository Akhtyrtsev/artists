from rest_framework import permissions


class SelfPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.groups.filter(name__in=['client']).exists():
            return True
        return False