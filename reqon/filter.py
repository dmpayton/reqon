import rethinkdb as r

from .geo import geojson_to_reql

# move build[_*] to utils.py?

def build(node):
    op, value = node
    if op in LOGIC_OPS:
        builder, func = LOGIC_OPS[op]
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
    if isinstance(value, list) and value[0] in BOOL_OPS:
        op, value = value
        func = BOOL_OPS[op]

    return func(row, value)


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
