from django.db import models
from django_hstore import hstore
from locations.models import Location
from workers.models import Worker


class Report(models.Model):
    location = models.ForeignKey(Location)
    reporter = models.ForeignKey(Worker)
    data = hstore.DictionaryField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = hstore.HStoreManager()
