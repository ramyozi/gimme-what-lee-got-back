from rest_framework.response import Response
from rest_framework import status
from functools import wraps

def allowed_roles(*roles):
    """
    Décorateur pour DRF view ou @action.
    Exemple : @allowed_roles("admin", "member")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
            if request.user.role not in roles:
                return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            return func(self, request, *args, **kwargs)
        return wrapper
    return decorator
