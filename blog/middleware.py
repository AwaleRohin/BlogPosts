import re
from BlogPosts import settings
from django.shortcuts import redirect

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip("/"))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip("/")
        is_url_exempt = any(url.match(path) for url in EXEMPT_URLS)
        if request.user.is_authenticated and is_url_exempt:
            return redirect(settings.LOGOUT_REDIRECT_URL)
        elif request.user.is_authenticated or is_url_exempt:
            return None
        else:
            return redirect(settings.LOGIN_URL)
