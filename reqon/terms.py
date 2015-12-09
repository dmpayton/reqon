import rethinkdb as r
import six

from .coerce import coerce
from .operators import build
from .exceptions import *
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
        Adds a filter to the query
        ['$filter', [
            ...
        ]]

        Arguments:
        reql -- The reql query to append to
        value -- The filter values to apply. This must be a list.

        Returns:
        A copy of the reql query with the filter(s) appended

        Exceptions:
        Raises a 'reqon.exceptions.InvalidFilterError' if any of the filters
        are invalid.
    '''
    if value:
        try:
            return reql.filter(
                r.and_(*map(build, value))
            )
        except:
            raise InvalidFilterError(ERRORS['filter']['invalid'].format(value))

    return reql


# Transformations


def has_fields(reql, value):
    '''
        Adds a 'has_fields' filter to the query
        ['$has_fields', ['name', 'birthday']]

        Arguments:
        reql -- The reql query to append to
        value -- The fields to include

        Returns:
        A copy of the reql query with the 'has_fields' filter appended

        Exceptions:
        No custom exceptions are currently raised
    '''
    value = [_expand_path(path) for path in value]
    return reql.has_fields(*value)


def with_fields(reql, value):
    '''
        Adds a 'with_fields' filter to the query
        ['$with_fields', ['name', 'birthday']]

        Arguments:
        reql -- The reql query to append to
        value -- The fields to include

        Returns:
        A copy of the reql query with the 'with_fields' filter appended

        Exceptions:
        No custom exceptions are currently raised
    '''
    value = [_expand_path(path) for path in value]
    return reql.with_fields(*value)


def order_by(reql, value):
    '''
        Adds an 'order_by' filter to the query
        ['$order_by', 'name']
        ['$order_by', ['$index', 'name']]

        Arguments:
        reql -- The reql query to append to
        value -- The field(s) to order by

        Returns:
        A copy of the reql query with the 'order_by' filter appended

        Exceptions:
        No custom exceptions are currently raised
    '''
    if isinstance(value, list) and value[0] == '$index':
        return reql.order_by(index=value[1])
    return reql.order_by(_expand_path(value))


def skip(reql, value):
    '''
        Adds a 'skip' filter to the query
        ['$skip', 10]

        Arguments:
        reql -- The reql query to append to
        value -- The number of records to skip

        Returns:
        A copy of the reql query with the 'skip' filter appended

        Exceptions:
        Raises a 'reqon.exceptions.TypeError' if value is not an integer
    '''
    if not isinstance(value, int):
        raise TypeError(ERRORS['type']['int'].format('skip'))
    return reql.skip(value)


def limit(reql, value):
    '''
        Adds a 'limit' filter to the query
        ['$limit', 10]

        Arguments:
        reql -- The reql query to append to
        value -- The maximum number of records to retrieve

        Returns:
        A copy of the reql query with the 'limit' filter appended

        Exceptions:
        Raises a 'reqon.exceptions.TypeError' if the value is not an integer
    '''
    if not isinstance(value, int):
        raise TypeError(ERRORS['type']['int'].format('limit'))
    return reql.limit(value)


def slice_(reql, value):
    '''
        Adds a 'slice' filter to the query
        ['$slice', [10, 20]]

        Arguments:
        reql -- The reql query to append to
        value -- A list of integers, noting the starting and ending indices
        to return from the query

        Returns:
        A copy of the reql query with the 'slice' filter appended

        Exceptions:
        Raises a 'reqon.exceptions.TypeError' if the value is not a list of integers
    '''
    if isinstance(value, list) and all(isinstance(x, int) for x in value):
        return reql.slice(*value)
    else:
        raise TypeError(ERRORS['type']['invalid'].format('slice'))


def nth(reql, value):
    '''
        Adds an 'nth' filter to the query
        ['$nth', 10]

        Arguments:
        reql -- The reql query to append to
        value -- An integer indicating the `nth` value to return from the query

        Returns:
        A copy of the reql query with the 'nth' filter appended

        Exceptions:
        Raises a 'reqon.exceptions.TypeError' if the value is not an integer
    '''
    if not isinstance(value, int):
        raise TypeError(ERRORS['type']['int'].format('nth'))
    return reql.nth(value)


def sample(reql, value):
    '''
        Adds a 'sample' filter to the query
        ['$sample', 10]

        Arguments:
        reql -- The reql query to append to
        value -- An integer indicating the number of values to sample from the result

        Returns:
        A copy of the reql query with the 'sample' filter appended

        Exceptions:
        Raises a 'reqon.exceptions.TypeError' if the value is not an integer
    '''
    if not isinstance(value, int):
        raise TypeError(ERRORS['type']['int'].format('sample'))
    return reql.sample(value)


# Manipulation


def pluck(reql, value):
    '''
        Adds a 'pluck' filter to the query
        ['$pluck', ['name', 'birthday']]

        Arguments:
        reql -- The reql query to append to
        value -- A list of strings indicating the field names to return

        Returns:
        A copy of the reql query with the 'pluck' filter appended

        Exceptions:
        Raises a 'reqon.exceptions.TypeError' if the value is not a list of strings
    '''
    if isinstance(value, list) and all(isinstance(x, six.string_types) for x in value):
        value = [_expand_path(path) for path in value]
        return reql.pluck(*value)
    else:
        raise TypeError(ERRORS['type']['invalid'].format('pluck'))


def without(reql, value):
    '''
        Adds a 'without' filter to the query
        ['$without', ['name', 'birthday']]

        Arguments:
        reql -- The reql query to append to
        value -- A list of strings indicating the fields to omit from the response

        Returns:
        A copy of the reql query with the 'without' filter appended

        Exceptions:
        Raises a 'reqon.exceptions.TypeError' if the value is not a list of strings
    '''
    if isinstance(value, list) and all(isinstance(x, six.string_types) for x in value):
        value = [_expand_path(path) for path in value]
        return reql.without(*value)
    else:
        raise TypeError(ERRORS['type']['invalid'].format('without'))


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
        'invalid': "Invalid type passed to {0}. Must be either a Number, String, Boolean, or Array",
        'int': "Invalid type passed to {0}. Must be a Integer."
    },
    'filter': {
        'invalid': "Invalid filter ReQON filter - {0} - passed to ReQON"
    }
}
