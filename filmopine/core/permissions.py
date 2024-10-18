from rest_framework import permissions 

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission class that allows safe methods for all users,
    while restricting unsafe methods to admin users only.

    This permission class checks the request method and grants access
    based on the following rules:
        - Allows GET, HEAD, and OPTIONS requests from any user (safe methods).
        - Allows PUT, PATCH, and DELETE requests only if the user is authenticated
          and has staff privileges (admin).

    Attributes:
        None

    Methods:
        has_permission(request, view): 
            Determines if the user has permission to perform the requested action.

    Returns:
        bool: True if the request is allowed, otherwise False.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # i.e., GET, HEAD, and OPTIONS
            return True # Anyone can access the target View
        
        return bool(request.user and request.user.is_staff) # Basically, if the user is logged in and is Admin (you can set this up via admin panel), then they can do the other operations (PUT, PATCH, DELETE)


class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission class that allows only admin users or the owner of an object
    to perform update and delete operations.

    This permission class enforces the following rules:
        - Allows only authenticated users to create reviews (POST requests).
        - Allows safe methods (GET, HEAD, OPTIONS) for all users.
        - For non-safe methods (PUT, PATCH, DELETE), it restricts access to
          either the admin users or the owner of the object.

    Attributes:
        None

    Methods:
        has_permission(request, view): 
            Determines if the user has permission to perform the requested action.

        has_object_permission(request, view, obj): 
            Determines if the user has permission to perform the action on a specific object.

    Returns:
        bool: True if the request is allowed, otherwise False.
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
