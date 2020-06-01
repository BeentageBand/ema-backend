from rest_framework.permissions import BasePermission, SAFE_METHODS


# Permission

class IsAdminOrReadOnly(BasePermission):
    """
    Admin Permissions and ReadOnly for other Users
    """
    message = 'User does not have Admin permissions.'

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS and request.user and request.user.is_authenticated or
                    request.user and request.user.is_staff and request.user.is_authenticated
                    )


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """
    message = 'User does not have write permissions.'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Instance must have an attribute named `owner`.
        return obj.user == request.user
