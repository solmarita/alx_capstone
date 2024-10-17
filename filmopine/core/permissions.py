from rest_framework import permissions 

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # i.e., GET, HEAD, and OPTIONS
            return True # Anyone can access the target View
        
        return bool(request.user and request.user.is_staff) # Basically, if the user is logged in and is Admin (you can set this up via admin panel), then they can do the other operations (PUT, PATCH, DELETE)


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission to allow only admins or the owner of the object to update/delete.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users to create reviews (POST)
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)

        # Safe methods (GET, HEAD, OPTIONS) are open to everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # For non-safe methods, permission check will be done per object
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Safe methods are allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Non-safe methods (PUT, PATCH, DELETE) are only allowed for the admin or the owner
        return bool(request.user and (request.user.is_staff or obj.user == request.user))
