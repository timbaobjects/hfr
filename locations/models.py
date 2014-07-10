from django.core.cache import cache, get_cache, InvalidCacheBackendError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import networkx as nx
from django.conf import settings

CACHE_KEY = 'locations_graph'
CACHE_KEY_R = 'reversed_locations_graph'


class LocationType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Location(MPTTModel):
    location_type = models.ForeignKey(LocationType, related_name='locations')
    name = models.CharField(max_length=100)
    code = models.CharField(db_index=True, max_length=30, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True)

    def __unicode__(self):
        return '{} {}'.format(self.name, self.location_type.name)

    @classmethod
    def get_by_code(cls, code):
        location = None
        try:
            location = cls.objects.get(code__iexact=code)
        except cls.DoesNotExist:
            pass

        return location

    @classmethod
    def _get_locations_graph(cls, reverse=False):
        if reverse:
            if not hasattr(cls, '_reversed_locations_graph'):
                cls._reversed_locations_graph = get_locations_graph(reverse)
            return cls._reversed_locations_graph
        else:
            if not hasattr(cls, '_locations_graph'):
                cls._locations_graph = get_locations_graph()
            return cls._locations_graph

    @property
    def node(self):
        graph = self._get_locations_graph()
        return graph.node[self.pk]

    def nx_descendants(self, include_self=False):
        graph = self._get_locations_graph()
        descendant_ids = nx.topological_sort(
            graph,
            graph.subgraph(nx.dfs_tree(graph, self.id).nodes()).nodes()
        )
        if include_self:
            return [graph.node[id] for id in descendant_ids]
        else:
            return [graph.node[id] for id in descendant_ids if id != self.id]

    def nx_ancestors(self, include_self=False):
        reversed_graph = self._get_locations_graph(reverse=True)
        ancestor_ids = nx.topological_sort(
            reversed_graph,
            reversed_graph.subgraph(
                nx.dfs_tree(reversed_graph, self.id).nodes()).nodes()
        )
        if include_self:
            return [reversed_graph.node[id] for id in ancestor_ids]
        else:
            return [reversed_graph.node[id]
                    for id in ancestor_ids if id != self.id]

    def nx_children(self):
        reversed_graph = self._get_locations_graph()
        children_ids = reversed_graph.successors(self.id)
        return [reversed_graph.node[id] for id in children_ids]


def get_locations_graph(reverse=False):
    try:
        app_cache = get_cache('graphs')
    except InvalidCacheBackendError:
        app_cache = cache

    graph = app_cache.get(CACHE_KEY_R) if reverse else app_cache.get(CACHE_KEY)
    if not graph:
        if reverse:
            graph = generate_locations_graph().reverse()
            app_cache.set(CACHE_KEY_R, graph,
                          settings.LOCATION_GRAPH_CACHE_LIFETIME)
        else:
            graph = generate_locations_graph()
            app_cache.set(CACHE_KEY, graph,
                          settings.LOCATION_GRAPH_CACHE_LIFETIME)
    return graph


def generate_locations_graph():
    location_qs = Location.objects.order_by('level', 'name').values(
        'pk', 'name', 'parent__pk', 'location_type__name')
    graph = nx.DiGraph()

    for loc_info in location_qs.filter(parent__pk=None):
        graph.add_node(loc_info['pk'], name=loc_info['name'],
                       id=loc_info['pk'], type=loc_info['location_type__name'])

    for loc_info in location_qs.exclude(parent__pk=None):
        graph.add_node(loc_info['pk'], name=loc_info['name'],
                       id=loc_info['pk'], type=loc_info['location_type__name'])
        graph.add_edge(loc_info['parent__pk'], loc_info['pk'])

    return graph
