import rethinkdb as r

from .filter import build


def filter(reql, value):
    return reql.filter(
        r.and_(*map(build, value))
    )


def get(reql, value):
    return reql.get(value)


def get_all(reql, value):
    index = 'id'
    if len(value) == 2 and isinstance(value[1], list):
        value, index = value
    return reql.get_all(*value, index=index)


def group(reql, value):
    return reql.group(value)


def has_fields(reql, value):
    return reql.has_fields(*value)


def limit(reql, value):
    return reql.limit(value)


def nth(reql, value):
    return reql.nth(value)


def skip(reql, value):
    return reql.skip(value)


def pluck(reql, value):
    return reql.pluck(*value)


def sample(reql, value):
    return reql.sample(value)


def slice(reql, value):
    return reql.slice(*value)


def without(reql, value):
    return reql.without(*value)


TERMS = {
    '$filter': filter,
    '$get': get,
    '$get_all': get_all,
    '$group': group,
    '$has_fields': has_fields,
    '$limit': limit,
    '$nth': nth,
    '$skip': skip,
    '$pluck': pluck,
    '$sample': sample,
    '$slice': slice,
    '$without': without,
}
