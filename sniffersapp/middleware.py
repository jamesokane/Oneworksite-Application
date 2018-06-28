from django.http import HttpResponseRedirect
from django.conf import settings
import re

LOGIN_URL = getattr(settings, 'LOGIN_URL', '/accounts/login/')
ADMIN_URL = getattr(settings, 'ADMIN_URL', '/admin/')

EXEMPT_URLS = (
    LOGIN_URL,
    ADMIN_URL,
    '/static',
    '/accounts',
)

def login_required_middleware(get_response):
    exempt_list = [re.compile(e.rstrip('/')) for e in EXEMPT_URLS]

    def middleware(request):
        if not request.user.is_authenticated and \
                not any(m.match(request.path) for m in exempt_list):
            return HttpResponseRedirect('%s?next=%s' % (LOGIN_URL, request.path))
        response = get_response(request)
        return response

    return middleware
