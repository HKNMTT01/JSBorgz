from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def roles_required(*roles):
    def outer(view):
        @login_required
        @wraps(view)
        def inner(request,*args,**kwargs):
            if request.user.is_superuser or request.user.role in roles: return view(request,*args,**kwargs)
            raise PermissionDenied
        return inner
    return outer
