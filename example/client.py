import copy
import datetime
import json


class Field(object):
    modifiers = ('date', 'time', 'year', 'month', 'day', 'hours', 'minutes',
        'seconds', 'day_of_month', 'day_of_year', 'timezone')
    operators = ('ieq', 'in', 'regex', 'starts', 'istarts', 'ends', 'iends',
        'intersects', 'includes')

    def __init__(self, field):
        self.field = field

    def __eq__(self, other):
        return [self.field, ['$eq', self._coerce(other)]]

    def __ne__(self, other):
        return [self.field, ['$ne', self._coerce(other)]]

    def __lt__(self, other):
        return [self.field, ['$lt', self._coerce(other)]]

    def __le__(self, other):
        return [self.field, ['$le', self._coerce(other)]]

    def __gt__(self, other):
        return [self.field, ['$gt', self._coerce(other)]]

    def __ge__(self, other):
        return [self.field, ['$ge', self._coerce(other)]]

    def __getattr__(self, attr):
        if attr in self.operators:
            return self._operator(attr)
        if attr in self.modifiers:
            return self._modifier(attr)
        raise AttributeError("'Field' object has no attribute '{0}'".format(attr))

    def _modifier(self, modifier):
        def inner():
            return Field('{0}.${1}'.format(self.field, modifier))
        return inner

    def _operator(self, operator):
        def inner(value):
            return [self.field, ['${0}'.format(operator), self._coerce(value)]]
        return inner

    def _coerce(self, value):
        if isinstance(value, datetime.datetime):
            return ['$datetime', str(value)]
        if isinstance(value, datetime.date):
            return ['$date', str(value)]
        if isinstance(value, datetime.time):
            return ['$time', str(value)]
        return value


class Query(object):
    def __init__(self, db=None, table=None):
        self.db = db
        self.table = table
        self.query = []

    @classmethod
    def AND(cls, *args):
        return ['$and', [args]]

    @classmethod
    def OR(cls, *args):
        return ['$or', [args]]

    @classmethod
    def NOT(cls, *args):
        return ['$not', [args]]

    def _clone(self):
        query = Query(db=self.db, table=self.table)
        query.query.extend(copy.deepcopy(self.query))
        return query

    def as_reqon(self):
        return {
            '$db': self.db,
            '$table': self.table,
            '$query': self.query
        }

    def as_json(self):
        return json.dumps(self.as_reqon())

    def append_term(self, term, **kwargs):
        if kwargs:
            self.query.append([term, kwargs])
        else:
            self.query.append([term, value])

    # Selecting data

    def get(self, pk):
        self.append_term('$get', key=pk)
        return self._clone()

    def get_all(self, keys, **kwargs):
        self.append_term('$get_all', keys=keys, **kwargs)
        return self._clone()

    def filter(self, *filters):
        self.append_term('$filter', predicate=filters)
        return self._clone()

    # Transformations

    def has_fields(self, *fields):
        self.append_term('$has_fields', fields=fields)
        return self._clone()

    def with_fields(self, *fields):
        self.append_term('$with_fields', fields=fields)
        return self._clone()

    def order_by(self, **kwargs):
        self.append_term('$order_by', **kwargs)
        return self._clone()

    def skip(self, n):
        self.append_term('$skip', n=n)
        return self._clone()

    def limit(self, n):
        self.append_term('$limit', n=n)
        return self._clone()

    def slice(self, start_offset, end_offset, **kwargs):
        self.append_term('$slice', start_offset=start_offset,
            end_offset=end_offset, **kwargs)
        return self._clone()

    def nth(self, n):
        self.append_term('$nth', n=n)
        return self._clone()

    def sample(self, n):
        self.append_term('$sample', n=n)
        return self._clone()

    # Manipulation

    def pluck(self, *fields):
        self.append_term('$pluck', fields=fields)
        return self._clone()

    def without(self, *fields):
        self.append_term('$without', fields=fields)
        return self._clone()

    # Aggregation

    def group(self, **kwargs):
        self.append_term('$group', **kwargs)
        return self._clone()

    def count(self):
        self.append_term('$count')
        return self._clone()

    def sum(self, field):
        self.append_term('$sum', field=field)
        return self._clone()

    def avg(self, field):
        self.append_term('$avg', field=field)
        return self._clone()

    def min(self, field):
        self.append_term('$min', field=field)
        return self._clone()

    def max(self, field):
        self.append_term('$max', field=field)
        return self._clone()

    # Geospatial

    def get_intersecting(self, geometry, index):
        self.append_term('$get_intersecting', geometry=geometry, index=index)
        return self._clone()

    def get_nearest(self, geometry, index, **kwargs):
        self.append_term('$get_nearest', geometry=geometry, index=index, **kwargs)
        return self._clone()
