import rethinkdb as r

from .operators import build


# Selecting data


def get(reql, value):
    '''
        ['get', 'abc']
    '''
    return reql.get(value)


def get_all(reql, value):
    '''
        ['get_all', ['abc', '123', ...]]
        ['get_all', ['name', ['abc', '123', ...]]]
    '''
    index = 'id'
    if len(value) == 2 and isinstance(value[1], list):
        index, value = value
    return reql.get_all(*value, index=index)


def filter_(reql, value):
    '''
        ['filter', [
            ...
        ]]
    '''
    return reql.filter(
        r.and_(*map(build, value))
    )


# Transformations


def has_fields(reql, value):
    '''
        ['has_fields', ['name', 'birthday']]
    '''
    return reql.has_fields(*value)


def with_fields(reql, value):
    '''
        ['with_fields', ['name', 'birthday']]
    '''
    return reql.with_fields(*value)


def order_by(reql, value):
    '''
        ['order_by', 'name']
        ['order_by', ['$index', 'name']]
    '''
    if isinstance(value, list) and value[0] == '$index':
        return reql.order_by(index=value[1])
    return reql.order_by(value)


def skip(reql, value):
    '''
        ['skip', 10]
    '''
    return reql.skip(value)


def limit(reql, value):
    '''
        ['limit', 10]
    '''
    return reql.limit(value)


def slice_(reql, value):
    '''
        ['slice', [10, 20]]
    '''
    return reql.slice(*value)


def nth(reql, value):
    '''
        ['nth', 10]
    '''
    return reql.nth(value)


def sample(reql, value):
    '''
        ['sample', 10]
    '''
    return reql.sample(value)


# Manipulation


def pluck(reql, value):
    '''
        ['pluck', ['name', 'birthday']]
    '''
    return reql.pluck(*value)


def without(reql, value):
    '''
        ['without', ['name', 'birthday']]
    '''
    return reql.without(*value)


# Aggregation


def group(reql, value):
    '''
        ['group', 'birthday']
        ['group', ['$index', 'birthday']]
    '''
    if isinstance(value, list) and value[0] == '$index':
        return reql.group(index=value[1])
    return reql.group(value)


def count(reql, value=None):
    '''
        ['count']
    '''
    if value:
        return reql.count(value)
    return reql.count()


def sum_(reql, value):
    '''
        ['sum', 'counter']
    '''
    return reql.sum(value)


def avg(reql, value):
    '''
        ['avg', 'points']
    '''
    return reql.avg(value)


def min_(reql, value):
    '''
        ['min', 'points']
    '''
    return reql.min(value)


def max_(reql, value):
    '''
        ['max', 'points']
    '''
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
    '$slice': slice_,
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
