from rest_framework import permissions


class WalletPermission(permissions.BasePermission):

    def has_object_permission(self, obj, view, request):
        return obj.user == request.user
