from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class LocationType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Location(MPTTModel):
    location_type = models.ForeignKey(LocationType, related_name='locations')
    name = models.CharField(max_length=100)
    code = models.CharField(db_index=True, max_length=30, unique=True)
    parent = TreeForeignKey('self', blank=True)

    def __unicode__(self):
        return '{} {}'.format(self.name, self.location_type.name)
