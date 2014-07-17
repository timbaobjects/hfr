from django_hstore.managers import HStoreManager
from core.querysets import LocationQuerySet


class ReportManager(HStoreManager):
    def get_query_set(self):
        return LocationQuerySet(self.model, using=self.db)
