from django.shortcuts import redirect
from functools import wraps

def superuser_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('core:home')
        
        if not request.user.is_superuser:
            return redirect('core:home')

        return view_func(request, *args, **kwargs)

    return _wrapped_view
