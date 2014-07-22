from dateutil.parser import parse
from django import forms
import django_filters
from rapidsms.contrib.messagelog.models import Message
from locations.models import Location, LocationType
from workers.models import Worker


def parse_date_range(value, sep='-'):
    '''Given two string representations of datetime values with
    a separator between them, attempts to parse for valid values.

    Requires python-dateutil.'''
    try:
        start, end = [parse(p) for p in value.split(sep)]
    except Exception:
        return None

    return start, end


class BaseDateTimeRangeFilter(django_filters.CharFilter):
    '''Uses `parse_date_range` to filter a queryset for records
    that have a property with the given `field_name` lying between
    the parsed dates, or an empty queryset if there is a parse error.

    Must be subclassed and `field_name` set to be useful, since
    the default implementation just raised `ValueError`.'''
    field_name = None

    def filter(self, qs, value):
        if not self.field_name:
            raise ValueError('Improperly configured: field_name must be set')

        field_kwarg_key = '{}__range'.format(self.field_name)

        if value:
            res = parse_date_range(value)
            if not res:
                return qs.none()

            return qs.filter(**{field_kwarg_key: res})

        return qs


class MessageDateTimeRangeFilter(BaseDateTimeRangeFilter):
    field_name = 'date'


class MessageDirectionFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [('', '-- Direction --')] + list(Message.DIRECTION_CHOICES)
        return super(MessageDirectionFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            return qs.filter(direction=value)

        return qs


class MessageConnectionFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(connection__identity__contains=value)

        return qs


class BaseLocationFilter(django_filters.CharFilter):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = forms.HiddenInput()

        return super(BaseLocationFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        raise NotImplementedError('Please subclass and implement filter()')


class ReportLocationFilter(BaseLocationFilter):
    def filter(self, qs, value):
        if value:
            try:
                location = Location.objects.get(pk=value)
                return qs.filter_in(location)
            except Location.DoesNotExist:
                return qs.none()

        return qs


class WorkerLocationFilter(BaseLocationFilter):
    def filter(self, qs, value):
        if value:
            try:
                location = Location.objects.get(pk=value)
                descendant_pks = [node['id']
                                  for node in location.nx_descendants(True)]
                return qs.filter(location__in=descendant_pks)
            except Location.DoesNotExist:
                return qs.none()

        return qs


class WorkerPhoneFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(contact__connection__identity__icontains=value)

        return qs


class MessageFilterSet(django_filters.FilterSet):
    direction = MessageDirectionFilter(label="",widget=forms.Select({
        'class': 'input-sm col-md-2 form-control','placeholder':'Direction'}))
    phone = MessageConnectionFilter(label="",widget=forms.TextInput({
        'class': 'form-control input-sm col-md-2','placeholder':'Phone'}))
    date_range = MessageDateTimeRangeFilter(label="",widget=forms.TextInput({
        'class': 'time-range input-sm col-md-2 form-control', 'placeholder':'Date Range'}))

    class Meta:
        model = Message
        fields = []


class WorkerFilterSet(django_filters.FilterSet):
    phone = WorkerPhoneFilter()

    class Meta:
        model = Worker
        fields = []
