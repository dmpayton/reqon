import datetime
import rethinkdb as r

from .geo import geojson_to_reql


def build(node):
    op, value = node
    if op in BOOLEAN:
        builder, func = BOOLEAN[op]
        return builder(value, func)
    return build_attribute(op, value)


def build_sequence(node, func):
    return func(*map(build, node))


def build_unary(node, func):
    return func(build(node))


def build_attribute(attrs, value):
    row = r.row
    for attr in attrs.split('.'):
        row = row[attr]

    func = r.eq  # equality by default
    if isinstance(value, list) and value[0] in EXPRESSIONS:
        op, value = value
        func = EXPRESSIONS[op]

    return func(row, value)


def in_(row, value):
    '''
        ['score', ['$in', [1, 2, 3, 4]]
    '''
    return r.expr(value).contains(row)


def regex(row, value):
    '''
        ['name', ['$regex', '^D']]
    '''
    return row.coerce_to('string').match(value)


def ieq(row, value):
    '''
        ['name', ['$ieq', 'derek']]
    '''
    return regex(row, '(?i)^{0}$'.format(value))


def starts(row, value):
    '''
        ['name', ['$starts', 'D']]
    '''
    return regex(row, '^{0}'.format(value))


def istarts(row, value):
    '''
        ['name', ['$istarts', 'd']]
    '''
    return regex(row, '(?i)^{0}'.format(value))


def ends(row, value):
    '''
        ['name', ['$ends', 'Y']]
    '''
    return regex(row, '{0}$'.format(value))


def iends(row, value):
    '''
        ['name', ['$iends', 'y']]
    '''
    return regex(row, '(?i){0}$'.format(value))


def includes(row, value):
    '''
        ['area', ['$includes', {
            'type': 'Point',
            'coordinates': [-135.4078334251454, -38.32676733670448]
        }]]
    '''
    shape = geojson_to_reql(value)
    return row.includes(shape)


def intersects(row, value):
    '''
        ['area', ['$intersects', {
            'type': 'Polygon',
            'coordinates': [[[-116, 28], [13, -26], [59, 58], [-116, 28]]]
        }]]
    '''
    shape = geojson_to_reql(value)
    return row.intersects(shape)


BOOLEAN = {
    '$and': (build_sequence, r.and_),
    '$or': (build_sequence, r.or_),
    '$not': (build_unary, r.not_),
}

EXPRESSIONS = {
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
    '$includes': includes,
}
