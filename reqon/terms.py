import rethinkdb as r

from .operators import build


# Selecting data


def get(reql, value):
    return reql.get(value)


def get_all(reql, value):
    index = 'id'
    if len(value) == 2 and isinstance(value[1], list):
        index, value = value
    return reql.get_all(*value, index=index)


def filter_(reql, value):
    return reql.filter(
        r.and_(*map(build, value))
    )


# Transformations


def has_fields(reql, value):
    return reql.has_fields(*value)


def with_fields(reql, value):
    return reql.with_fields(*value)


def order_by(reql, value):
    if isinstance(value, list) and value[0] == '$index':
        return reql.order_by(index=value[1])
    return reql.order_by(value)


def skip(reql, value):
    return reql.skip(value)


def limit(reql, value):
    return reql.limit(value)


def slice(reql, value):
    return reql.slice(*value)


def nth(reql, value):
    return reql.nth(value)


def sample(reql, value):
    return reql.sample(value)


# Manipulation


def pluck(reql, value):
    return reql.pluck(*value)


def without(reql, value):
    return reql.without(*value)


# Aggregation


def group(reql, value):
    if isinstance(value, list) and value[0] == '$index':
        return reql.group(index=value[1])
    return reql.group(value)


def count(reql, value=None):
    if value:
        return reql.count(value)
    return reql.count()


def sum_(reql, value):
    return reql.sum(value)


def avg(reql, value):
    return reql.avg(value)


def min_(reql, value):
    return reql.min(value)


def max_(reql, value):
    return reql.max(value)



TERMS = {
    '$get': get,
    '$get_all': get_all,
    '$filter': filter_,

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
    '$sum': sum_,
    '$avg': avg,
    '$min': min_,
    '$max': max_,
}
