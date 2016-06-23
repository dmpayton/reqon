import functools
import rethinkdb as r
import six
import dateutil.parser

from calendar import datetime

from . import utils
from .coerce import coerce
from .exceptions import ReqonError, FilterError
from .geo import geojson_to_reql
from .operators import build


# Selecting data


def get(reql, key):
    return reql.get(key)


def get_all(reql, keys, index='id'):
    return reql.get_all(*coerce(keys), index=index)


def filter(reql, predicate, default=False):
    for item in predicate:
        try:
            reql = reql.filter(build(item), default=default)
        except Exception:
            raise ReqonError('Invalid filter: {0}'.format(item))
    return reql


def between(reql, lower_key, upper_key, **kwargs):
    lower_key = coerce(lower_key)
    upper_key = coerce(upper_key)
    return reql.between(lower_key, upper_key, **kwargs)


# Transformations


def has_fields(reql, fields):
    return reql.has_fields(*utils.expand_paths(fields))


def with_fields(reql, fields):
    return reql.with_fields(*utils.expand_paths(fields))


def order_by(reql, key=None, index=None, ordering=None):
    if key is None and index is None:
        raise ReqonError('order_by requires a key or index')
    if key and index:
        raise ReqonError('order_by requires a key or index, but not both')

    try:
        ordering = {
            '$asc': r.asc,
            '$desc': r.desc,
            None: lambda x: x
        }[ordering]
    except KeyError:
        raise ReqonError('ordering must be "$asc" or "$desc"')

    if index:
        return reql.order_by(index=ordering(index))
    return reql.order_by(ordering(utils.expand_path(key)))


def skip(reql, n):
    return reql.skip(n)


def limit(reql, n):
    return reql.limit(n)


def slice(reql, start_offset, end_offset, **kwargs):
    return reql.slice(start_offset, end_offset, **kwargs)


def nth(reql, n):
    return reql.nth(n)


def sample(reql, n):
    return reql.sample(n)


# Manipulation


def pluck(reql, fields):
    return reql.pluck(*utils.expand_paths(fields))


def without(reql, fields):
    return reql.without(*utils.expand_paths(fields))


# Aggregation


def group(reql, field=None, index=None, multi=False):
    if field is None and index is None:
        raise ReqonError('group requires a field or index')
    if field and index:
        raise ReqonError('group requires a field or index, but not both')

    if index:
        return reql.group(index=index, multi=multi)
    return reql.group(utils.expand_path(field), multi=multi)


def count(reql):
    return reql.count()


def sum(reql, field):
    return reql.sum(utils.expand_path(field))


def avg(reql, field):
    return reql.avg(utils.expand_path(field))


def min(reql, field):
    return reql.min(utils.expand_path(field))


def max(reql, field):
    return reql.max(utils.expand_path(field))


# Geospatial


def get_intersecting(reql, geometry, index):
    geometry = geojson_to_reql(geometry)
    return reql.get_intersecting(geometry, index=index)


def get_nearest(reql, geometry, index, **kwargs):
    geometry = geojson_to_reql(geometry)
    return reql.get_nearest(geometry, index=index, **kwargs)


READ_TERMS = {
    '$get': get,
    '$get_all': get_all,
    '$filter': filter,
    '$between': between,

    '$has_fields': has_fields,
    '$with_fields': with_fields,
    '$order_by': order_by,
    '$skip': skip,
    '$limit': limit,
    '$slice': slice,
    '$nth': nth,
    '$sample': sample,

    '$pluck': pluck,
    '$without': without,

    '$group': group,
    '$count': count,
    '$sum': sum,
    '$avg': avg,
    '$min': min,
    '$max': max,

    '$get_intersecting': get_intersecting,
    '$get_nearest': get_nearest,
}


# TODO:
# WRITE_TERMS = {
#     '$insert': insert,
#     '$update': update,
#     '$replace': replace,
# }


def delete(reql, durability='hard', return_changes=False):
    return reql.delete(durability, return_changes)

DELETE_TERMS = {
    '$delete': delete,
}


def gather_terms(allow_delete=False):
    terms = {}
    terms.update(READ_TERMS)
    if allow_delete:
        terms.update(DELETE_TERMS)
    return terms

# All terms in one dict
TERMS = gather_terms(allow_delete=True)
