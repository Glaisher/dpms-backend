from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin()


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_employee()


class IsSecurity(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_security()

