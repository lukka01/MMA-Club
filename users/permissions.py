#წვდომის კონტროლი როლების მიხედვით
from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    #უფლება მარტო ადმინისტრატორს აქვს
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrCoach(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_admin or request.user.is_coach)
        )


class IsOwnerOrAdmin(BasePermission):
    #ან საკუთარ პროფილი, ან ადმინი
    def has_object_permission(self, request, view, obj):
        return request.user.is_admin or obj == request.user

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user