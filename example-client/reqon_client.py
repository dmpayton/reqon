import copy
import json


class NoValue(object):
    pass


def AND(*args):
    return ['$and', [args]]


def OR(*args):
    return ['$or', [args]]


def NOT(*args):
    return ['$or', [args]]


class row(object):
    modifiers = ('date', 'time', 'year', 'month', 'day', 'hours', 'minutes',
        'seconds', 'day_of_month', 'day_of_year', 'timezone')
    operators = ('ieq', 'in', 'regex', 'starts', 'istarts', 'ends', 'iends',
        'intersects', 'includes')

    def __init__(self, field):
        self.field = field

    def __eq__(self, other):
        return [self.field, ['$eq', other]]

    def __ne__(self, other):
        return [self.field, ['$ne', other]]

    def __lt__(self, other):
        return [self.field, ['$lt', other]]

    def __le__(self, other):
        return [self.field, ['$le', other]]

    def __gt__(self, other):
        return [self.field, ['$gt', other]]

    def __ge__(self, other):
        return [self.field, ['$ge', other]]

    def __contains__(self, item):
        return [self.field, ['$contains', item]]

    def __getattr__(self, attr):
        if attr in self.operators:
            return self._operator(attr)
        if attr in self.modifiers:
            return self._modifier(attr)
        raise AttributeError("'row' object has no attribute '{0}'".format(attr))

    def _modifier(self, modifier):
        def inner():
            return row('{0}.${1}'.format(self.field, modifier))
        return inner

    def _operator(self, operator):
        def inner(value):
            return [self.field, ['${0}'.format(operator), value]]
        return inner


class Query(object):
    def __init__(self, db=None, table=None, query=None):
        self.db = db
        self.table = table
        self.query = query or []

    def _clone(self):
        query = Query(db=self.db, table=self.table,
            query=copy.deepcopy(self.query))
        return query

    def as_reqon(self):
        return {
            '$db': self.db,
            '$table': self.table,
            '$query': self.query
        }

    def as_json(self):
        return json.dumps(self.as_reqon())

    def append_term(self, term, value=NoValue):
        if value == NoValue:
            self.query.append([term])
        else:
            self.query.append([term, value])

    def get(self, pk):
        self.append_term('$get', pk)
        return self._clone()

    def get_all(self, *pks):
        self.append_term('$get_all', pks)
        return self._clone()

    def filter(self, *filters):
        self.append_term('$filter', filters)
        return self._clone()

    def has_fields(self, *fields):
        self.append_term('$has_fields', fields)
        return self._clone()

    def with_fields(self, *fields):
        self.append_term('$with_fields', fields)
        return self._clone()

    def order_by(self, field):
        self.append_term('$order_by', field)
        return self._clone()

    def skip(self, num):
        self.append_term('$skip', num)
        return self._clone()

    def limit(self, num):
        self.append_term('$limit', num)
        return self._clone()

    def slice(self, start, end):
        self.append_term('$slice', [start, end])
        return self._clone()

    def nth(self, num):
        self.append_term('$nth', num)
        return self._clone()

    def sample(self, num):
        self.append_term('$sample', num)
        return self._clone()

    def pluck(self, *fields):
        self.append_term('$pluck', fields)
        return self._clone()

    def without(self, *fields):
        self.append_term('$without', fields)
        return self._clone()

    def group(self):
        return self._clone()

    def count(self):
        self.append_term('$count')
        return self._clone()

    def sum(self):
        self.append_term('$sum')
        return self._clone()

    def avg(self):
        self.append_term('$avg')
        return self._clone()

    def min(self):
        self.append_term('$min')
        return self._clone()

    def max(self):
        self.append_term('$max')
        return self._clone()
