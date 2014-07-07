from django.db import models
from locations.models import Location


class Role(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30)


class Worker(models.Model):
    role = models.ForeignKey(Role)
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Location)
