from django_hstore.query import HStoreQuerySet
from pandas import DataFrame, isnull


class LocationQuerySet(HStoreQuerySet):
    def filter_in(self, location):
        subloc_pks = [node.get('id', None)
                      for node in location.nx_descendants()]

        return self.filter(location__in=subloc_pks)

    def to_dataframe(self):
        subset = list(self.values('location', 'updated', 'data'))
        df = DataFrame(subset)

        data_series = df.pop('data').tolist()
        temp = [row if not isnull(row) else row for row in data_series]

        return df.join(DataFrame(temp)).convert_objects(convert_numeric=True)
