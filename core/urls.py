from django.conf.urls import include, patterns, url
from core.views import DashboardView

urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^accounts/login/?$', 'core.views.signin', name='signin'),
    url(r'^accounts/logout/?$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='signout'),
)
