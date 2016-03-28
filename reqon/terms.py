import functools
import rethinkdb as r
import six
import dateutil.parser

from .coerce import coerce
from .operators import build
from .exceptions import InvalidTypeError, InvalidFilterError
from .utils import dict_in
from calendar import datetime


def type_check(*args):
    outer_args = args

    def checker(func):
        @functools.wraps(func)
        def wrapper(*args):
            if outer_args[0] == six.string_types:
                if not isinstance(args[1], six.string_types):
                    raise InvalidTypeError(ERRORS['type']['string'].format(func.__name__))
            elif outer_args[0] == list:
                if not isinstance(args[1], list):
                    raise InvalidTypeError(ERRORS['type']['invalid'].format(func.__name__))
                if not all(isinstance(x, outer_args[1]) for x in args[1]):
                    raise InvalidTypeError(ERRORS['type']['invalid'].format(func.__name__))
            else:
                if not isinstance(args[1], outer_args[0]):
                    raise InvalidTypeError(ERRORS['type'][outer_args[0].__name__].format(func.__name__))
            return func(*args)
        return wrapper

    return checker


def _expand_path(fields):
    '''
        Break a dot-notated path into a dict

        Arguments:
        fields -- a string containing one or more dot-notated paths ('foo.bar')

        Returns:
        A dictionary representing the dot-notated paths
        { "foo": { "bar": True } }

        Exceptions:
        Raises a "reqon.exceptions.InvalidTypeError" if the argument is not a String
    '''

    if isinstance(fields, six.string_types):
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
    else:
        return fields


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
        Raises a "reqon.exceptions.InvalidTypeError" if the value contains a dict
    '''

    if isinstance(value, dict) or dict_in(value):
        raise InvalidTypeError(ERRORS['type']['invalid'].format('get'))
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
            for item in value:
                reql = reql.filter(build(item))
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
        ['$order_by', ['name', '$desc']]
        ['$order_by', ['$index', 'name']]
        ['$order_by', ['$index', 'name', $asc']]

        Arguments:
        reql -- The reql query to append to
        value -- The field(s) to order by

        Returns:
        A copy of the reql query with the 'order_by' filter appended

        Exceptions:
        No custom exceptions are currently raised
    '''
    if isinstance(value, list) and value[0] == '$index':
        if len(value) == 2:
            return reql.order_by(index=value[1])
        elif len(value) == 3 and value[2] == '$asc':
            return reql.order_by(index=r.asc(value[1]))
        elif len(value) == 3 and value[2] == '$desc':
            return reql.order_by(index=r.desc(value[1]))
    elif isinstance(value, list) and value[1] == '$asc':
        return reql.order_by(r.asc(value[0]))
    elif isinstance(value, list) and value[1] == '$desc':
        return reql.order_by(r.desc(value[0]))
    return reql.order_by(_expand_path(value))


@type_check(int)
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
        Raises a 'reqon.exceptions.InvalidTypeError' if value is not an integer
    '''
    return reql.skip(value)


@type_check(int)
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
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not an integer
    '''
    return reql.limit(value)

@type_check(list, int)
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
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not a list of integers
    '''
    return reql.slice(*value)


@type_check(int)
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
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not an integer
    '''
    return reql.nth(value)


@type_check(int)
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
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not an integer
    '''
    return reql.sample(value)


# Manipulation


@type_check(list, six.string_types)
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
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not a list of strings
    '''
    value = [_expand_path(path) for path in value]
    return reql.pluck(*value)


@type_check(list, six.string_types)
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
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not a list of strings
    '''
    value = [_expand_path(path) for path in value]
    return reql.without(*value)


# Aggregation


def group(reql, value):
    '''
        Adds a 'group' aggregation to the query
        ['$group', 'birthday']
        ['$group', ['$index', 'birthday']]

        Arguments:
        reql -- The reql query to append to
        value -- A string or list of [<index>, <string>] to group by

        Returns:
        A copy of the reql query with the 'group' aggregation appended

        Exceptions:
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not a string or list of strings
    '''
    if isinstance(value, list) and value[0] == '$index':
        if all(isinstance(x, six.string_types) for x in value):
            return reql.group(index=value[1])
        else:
            raise InvalidTypeError(ERRORS['type']['invalid'].format('group'))
    else:
        if isinstance(value, six.string_types):
            return reql.group(_expand_path(value))
        else:
            raise InvalidTypeError(ERRORS['type']['invalid'].format('group'))


def count(reql, value=None):
    '''
        Adds a 'count' aggregation to the query
        ['$count']

        Arguments:
        reql -- The reql query to append to

        Returns:
        The reql query with the 'count' aggregation appended to it

        Exceptions:
        Does not raise a custom exception
    '''
    if value:
        return reql.count(value)
    return reql.count()


@type_check(six.string_types)
def sum_(reql, value):
    '''
        Adds a 'sum' aggregation to the query
        ['$sum', 'counter']

        Arguments:
        reql -- The reql query to append to
        value -- The field to sum by

        Returns:
        The reql query with the 'sum' aggregation appended to it

        Exceptions:
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not a string
    '''
    return reql.sum(_expand_path(value))


@type_check(six.string_types)
def avg(reql, value):
    '''
        Adds an 'avg' aggregation to the query
        ['$avg', 'points']

        Arguments:
        reql -- The reql query to append to
        value -- The field to avg by

        Returns:
        The reql query with the 'sum' aggregation appended to it

        Exceptions:
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not a string
    '''
    return reql.avg(_expand_path(value))


@type_check(six.string_types)
def min_(reql, value):
    '''
        Adds a 'min' aggregation to the query
        ['$min', 'points']

        Arguments:
        reql -- The reql query to append to
        value -- The field to min by

        Returns:
        The reql query with the 'min' aggregation appended to it

        Exceptions:
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not a string
    '''
    return reql.min(_expand_path(value))


@type_check(six.string_types)
def max_(reql, value):
    '''
        Adds a 'max' aggregation to the query
        ['$max', 'points']

        Arguments:
        reql -- The reql query to append to
        value -- The field to max by

        Returns:
        The reql query with the 'max' aggregation appended to it

        Exceptions:
        Raises a 'reqon.exceptions.InvalidTypeError' if the value is not a string
    '''
    return reql.max(_expand_path(value))

def between(reql, args):
    '''
        Adds a 'between' filter to the query
        ['$between', ['2016-01-01', '2016-01-31', 'timestamp']]

        Arguments:
        reql -- The reql query to append to
        _from -- The starting timestamp
        _to -- The ending timestamp
        index -- The index to use for the filter

        Returns:
        The reql query with the 'between' filter appended to it
    '''
    def parse_arg(value):
        try:
            return dateutil.parser.parse(value)
        except ValueError:
            return value

    def get_time_zone(value):
        try:
            return value.isoformat().split('+')[1]
        except:
            return 'Z'

    if len(args) == 2:
        _from, _to = args
        index = None
    else:
        _from, _to, index = args

    options = {}

    if index:
       options['index'] = index

    if isinstance(_from, int):
        return reql.between(_from, _to, **options)

    lower = parse_arg(_from)
    upper = parse_arg(_to)

    if isinstance(lower, datetime.datetime) and isinstance(upper, datetime.datetime):
        timezone = get_time_zone(lower)
        return reql.between(
            r.time(lower.year, lower.month, lower.day, lower.hour, lower.minute, lower.second, timezone),
            r.time(upper.year, upper.month, upper.day, upper.hour, upper.minute, upper.second, timezone),
            **options
        )
    else:
        return reql.between(lower, upper, **options)


TERMS = {
    '$get': get,
    '$get_all': get_all,
    '$filter': filter_,
    '$between': between,

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
