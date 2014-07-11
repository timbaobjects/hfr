from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.decorator import method_decorator
from django.views.generic import ListView
from rapidsms.contrib.messagelog.models import Message
from core.models import Report


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
        self.filter_set = self.filter_class(
            request.GET,
            queryset=self.model._default_manager.all())

        self.object_list = self.get_queryset()
        context = self.get_context_data(object_list=self.object_list)

        return self.render_to_response(context)


class MessageListView(ListView):
    context_object_name = 'messages'
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
        context['user'] = self.user
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
