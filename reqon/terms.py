import rethinkdb as r

from .coerce import coerce
from .operators import build
from .exceptions import TypeError
from .utils import dict_in


def _expand_path(fields):
    '''
        Break a dot-notated path into a dict

        Arguments:
        fields -- a string containing one or more dot-notated paths ('foo.bar')

        Returns:
        A dictionary representing the dot-notated paths
        { "foo": { "bar": True } }

        Exceptions:
        Raises a "reqon.exceptions.TypeError" if the argument is not a String
    '''

    try:
        fields = fields.split('.')
        num_fields = len(fields)
        if num_fields == 1:
            return fields[0]
        row = node = {}
        for idx, field in enumerate(fields):
            if idx + 1 == num_fields:
                node[field] = True
            else:
                node[field] = {}
                node = node[field]
        return row
    except:
        raise TypeError(ERRORS['type']['string'].format('expand_path'))


# Selecting data


def get(reql, value):
    '''
        Add a "get" method to the query
        ['$get', 'abc']

        Arguments:
        reql -- The reql query to append to
        value -- One of a Number, String, Boolean, or List of one of these

        Returns:
        A copy of the reql query with the "get" method appended

        Exceptions:
        Raises a "reqon.exceptions.TypeError" if the value contains a dict
    '''

    if isinstance(value, dict) or dict_in(value):
        raise TypeError(ERRORS['type']['invalid'].format('get'))
    return reql.get(coerce(value))


def get_all(reql, value):
    '''
        Add a "get_all" method to the query
        ['$get_all', ['abc', '123', ...]]
        ['$get_all', ['name', ['abc', '123', ...]]]

        Arguments:
        reql -- The reql query to append to
        value -- A list containing one of the following:
            * The id's of the documents to retrieve
            * The index to use when fetching documents as the first element
              in the list, followed by another list of values to match on.

        Returns:
        A copy of the reql query with the "get_all" method appended

        Exceptions:
        No custom exceptions are currently raised
    '''
    index = 'id'
    if len(value) == 2 and isinstance(value[1], list):
        index, value = value
    return reql.get_all(*coerce(value), index=index)


def filter_(reql, value):
    '''
        ['filter', [
            ...
        ]]
    '''
    if value:
        return reql.filter(
            r.and_(*map(build, value))
        )
    return reql


# Transformations


def has_fields(reql, value):
    '''
        ['has_fields', ['name', 'birthday']]
    '''
    value = [_expand_path(path) for path in value]
    return reql.has_fields(*value)


def with_fields(reql, value):
    '''
        ['with_fields', ['name', 'birthday']]
    '''
    value = [_expand_path(path) for path in value]
    return reql.with_fields(*value)


def order_by(reql, value):
    '''
        ['order_by', 'name']
        ['order_by', ['$index', 'name']]
    '''
    if isinstance(value, list) and value[0] == '$index':
        return reql.order_by(index=value[1])
    return reql.order_by(_expand_path(value))


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
    value = [_expand_path(path) for path in value]
    return reql.pluck(*value)


def without(reql, value):
    '''
        ['without', ['name', 'birthday']]
    '''
    value = [_expand_path(path) for path in value]
    return reql.without(*value)


# Aggregation


def group(reql, value):
    '''
        ['group', 'birthday']
        ['group', ['$index', 'birthday']]
    '''
    if isinstance(value, list) and value[0] == '$index':
        return reql.group(index=value[1])
    return reql.group(_expand_path(value))


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
    return reql.sum(_expand_path(value))


def avg(reql, value):
    '''
        ['avg', 'points']
    '''
    return reql.avg(_expand_path(value))


def min_(reql, value):
    '''
        ['min', 'points']
    '''
    return reql.min(_expand_path(value))


def max_(reql, value):
    '''
        ['max', 'points']
    '''
    return reql.max(_expand_path(value))



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

ERRORS = {
    'type': {
        'string': "Invalid type passed to {0}. Must be a String.",
        'invalid': "Invalid type passed to {0}. Must be either a Number, String, Boolean, or Array"
    }
}
