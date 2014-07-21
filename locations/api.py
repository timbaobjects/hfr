from tastypie import fields
from tastypie.constants import ALL
from tastypie.resources import ModelResource
from locations.models import Location, LocationType


class LocationTypeResource(ModelResource):
    class Meta:
        queryset = LocationType.objects.all()
        resource_name = 'locationtypes'


class LocationResource(ModelResource):
    location_type = fields.ForeignKey(LocationTypeResource, 'location_type',
                                      full=True)

    class Meta:
        queryset = Location.objects.all()
        resource_name = 'locations'
        filtering = {
            'name': ALL
        }
