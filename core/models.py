from django.db import models
from django_hstore import hstore
from checklists.models import Form
from locations.models import Location
from workers.models import Worker
from .managers import ReportManager


class Report(models.Model):
    form = models.ForeignKey(Form, blank=True, null=True)
    location = models.ForeignKey(Location)
    reporter = models.ForeignKey(Worker)
    data = hstore.DictionaryField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ReportManager()
