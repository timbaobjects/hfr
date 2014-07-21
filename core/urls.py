from django.conf.urls import include, patterns, url
from tastypie.api import Api
from core.views import (
    DashboardView, MessageListView, ReportEditView, ReportListView,
    WorkerListView)
from locations.api import LocationResource, LocationTypeResource


v1_api = Api(api_name='v1')
v1_api.register(LocationResource())
v1_api.register(LocationTypeResource())

urlpatterns = patterns(
    '',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^messages/?$', MessageListView.as_view(), name='messages'),
    url(r'^personnel/?$', WorkerListView.as_view(), name='personnel'),
    url(r'^report/(?P<pk>\d+)/?$', ReportEditView.as_view(), name='report_edit'),
    url(r'^reports/?$', ReportListView.as_view(), name='reports'),
    url(r'^accounts/login/?$', 'core.views.signin', name='signin'),
    url(r'^accounts/logout/?$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='signout'),
)
