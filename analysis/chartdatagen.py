import numpy as np
from locations.models import Location


def get_base_chart_data(queryset, tags=None):
    dataframe = queryset.to_dataframe()
    locations = set(dataframe.get('location'))
    grouped = dataframe.groupby('location')

    if tags:
        data = {
            loc: grouped.get_group(loc).set_index('updated').resample(
                'M', how=np.sum)[tags] for loc in locations
        }
    else:
        data = {
            loc: grouped.get_group(loc).set_index('updated').resample(
                'M', how=np.sum) for loc in locations
        }

    return data
