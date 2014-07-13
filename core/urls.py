from django.conf.urls import include, patterns, url
from core.views import DashboardView, MessageListView, ReportListView, WorkerListView

urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^messages/?$', MessageListView.as_view(), name='messages'),
    url(r'^personnel/?$', WorkerListView.as_view(), name='personnel'),
    url(r'^reports/?$', ReportListView.as_view(), name='reports'),
    url(r'^accounts/login/?$', 'core.views.signin', name='signin'),
    url(r'^accounts/logout/?$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='signout'),
)
