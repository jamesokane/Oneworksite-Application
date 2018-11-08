from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from sniffersapp.dashboard.views import dashboard

urlpatterns = [
    path('', dashboard, name='home'),
    path('users/', include('sniffersapp.user_profile.urls')),
    path('accounts/', include('allauth.urls')),
    path('invitations/', include('invitations.urls')),
    path('connections/', include('sniffersapp.connections.urls')),
    path('equipment/', include('sniffersapp.equipment.urls')),
    path('projects/', include('sniffersapp.projects.urls')),
    path('dockets/', include('sniffersapp.daily_dockets.urls')),
    path('timesheets/', include('sniffersapp.timesheet.urls')),
    path('create_forms/', include('sniffersapp.create_forms.urls')),

    path('admin/', admin.site.urls),

    path(r'', include('django_select2.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    from django.views import defaults as default_views
    urlpatterns += [
        path('400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('403/', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
