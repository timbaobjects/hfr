from dateutil.parser import parse
from django import forms
import django_filters
from rapidsms.contrib.messagelog.models import Message


def parse_date_range(value, sep='-'):
    try:
        start, end = [parse(p) for p in value.split(sep)]
    except Exception:
        return None

    return start, end


class MessageDateTimeRangeFilter(django_filters.CharFilter):
    def filter(self, qs, value):
        if value:
            res = parse_date_range(value)
            if not res:
                return qs

            return qs.filter(date__range=res)

        return qs


class MessageDirectionFilter(django_filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = [(None, '')] + list(Message.DIRECTION_CHOICES)
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


class MessageFilterSet(django_filters.FilterSet):
    direction = MessageDirectionFilter()
    phone = MessageConnectionFilter()
    date_range = MessageDateTimeRangeFilter(widget=forms.TextInput({
        'class': 'datetimepicker'}))

    class Meta:
        model = Message
        fields = []
