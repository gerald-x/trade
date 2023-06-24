from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse


def user_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or HttpResponse.status_code == 403:
            return redirect(reverse('user:index') + f'?next={request.path}')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_admin:
                return redirect(reverse('adminUser:login') + f'?msg=true')
        if not request.user.is_authenticated or HttpResponse.status_code == 403:
            return redirect(reverse('adminUser:login') + f'?next={request.path}')
        return view_func(request, *args, **kwargs)
    return wrapper
