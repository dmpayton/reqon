import rethinkdb as r

from .build import build_sequence, build_unary
from .geo import geojson_to_reql


def in_(row, value):
    return r.expr(value).contains(row)


def regex(row, value):
    return row.coerce_to('string').match(value)


def ieq(row, value):
    return regex(row, '(?i)^{0}$'.format(value))


def starts(row, value):
    return regex(row, '^{0}'.format(value))


def istarts(row, value):
    return regex(row, '(?i)^{0}'.format(value))


def ends(row, value):
    return regex(row, '{0}$'.format(value))


def iends(row, value):
    return regex(row, '(?i){0}$'.format(value))


def includes(row, value):
    shape = geojson_to_reql(value)
    return row.includes(shape)


def intersects(row, value):
    shape = geojson_to_reql(value)
    return row.intersects(shape)


LOGIC_OPS = {
    '$and': (build_sequence, r.and_),
    '$or': (build_sequence, r.or_),
    '$not': (build_unary, r.not_),
}

BOOL_OPS = {
    '$eq': r.eq,
    '$ieq': ieq,
    '$ne': r.ne,
    '$gt': r.gt,
    '$ge': r.ge,
    '$lt': r.lt,
    '$le': r.le,
    '$in': in_,
    '$regex': regex,
    '$starts': starts,
    '$istarts': istarts,
    '$ends': ends,
    '$iends': iends,
    '$intersects': intersects,
    '$includes': intersects,
}
