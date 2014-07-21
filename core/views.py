from django.contrib.auth import REDIRECT_FIELD_NAME, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.generic import ListView, UpdateView, View
from django.views.generic.base import TemplateResponseMixin
from rapidsms.contrib.messagelog.models import Message
from checklists.models import Form
from core.filters import MessageFilterSet
from core.forms import generate_report_edit_form
from core.models import Report
from workers.models import Worker


def signin(request):
    request.session.clear()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            next_url = request.REQUEST.get(REDIRECT_FIELD_NAME, '')

            if not is_safe_url(url=next_url, host=request.get_host()):
                next_url = settings.LOGIN_REDIRECT_URL

            return HttpResponseRedirect(next_url)
    else:
        form = AuthenticationForm(request)

    context = RequestContext(request, {'form': form, 'page_title': 'Login'})

    return render_to_response('core/login.html', context)


class DashboardView(View, TemplateResponseMixin):
    template_name = 'core/index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class FilteredListView(ListView):
    filter_class = None
    filter_form_helper = None

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(FilteredListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.filter_form_helper:
            self.filter_set.form.helper = self.filter_form_helper

        context = super(FilteredListView, self).get_context_data(**kwargs)
        context['filter_form'] = self.filter_set.form
        context['user'] = self.user
        context['page_title'] = self.page_title

        return context

    def get_queryset(self):
        return self.filter_set.qs

    def get(self, request, *args, **kwargs):
        if self.model:
            qs = self.model._default_manager.all()
        else:
            qs = self.queryset
        self.filter_set = self.filter_class(
            request.GET,
            queryset=qs)

        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)

        return self.render_to_response(context)


class MessageListView(FilteredListView):
    context_object_name = 'msgs'
    filter_class = MessageFilterSet
    page_title = 'Messages'
    paginate_by = settings.PAGE_SIZE
    queryset = Message.objects.order_by('-pk')
    template_name = 'core/message_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(MessageListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class ReportListView(ListView):
    context_object_name = 'reports'
    page_title = 'Reports'
    paginate_by = settings.PAGE_SIZE
    queryset = Report.objects.order_by('-updated')
    template_name = 'core/report_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ReportListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)
        context['checklist'] = Form.objects.first()
        context['page_title'] = self.page_title
        return context


class WorkerListView(ListView):
    context_object_name = 'workers'
    page_title = 'Personnel'
    paginate_by = settings.PAGE_SIZE
    queryset = Worker.objects.all()
    template_name = 'core/worker_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(WorkerListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context


class ReportEditView(UpdateView):
    page_title = 'Edit report'
    template_name = 'core/report_edit.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.report = get_object_or_404(Report, pk=kwargs['pk'])
        self.form_class = generate_report_edit_form(self.report.form)
        return super(ReportEditView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReportEditView, self).get_context_data(**kwargs)

        return context

    def get_object(self):
        return self.report

    def get_success_url(self):
        return reverse('reports')
