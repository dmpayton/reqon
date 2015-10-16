import rethinkdb as r

from .filter import build

'''
def (reql, value):
    reql.(value)
'''

def filter(reql, value):
    return reql.filter(
        r.and_(*map(build, value))
    )

def group(reql, value):
    return reql.group(value)


def has_fields(reql, value):
    return reql.has_fields(*value)


def limit(reql, value):
    return reql.limit(value)


def nth(reql, value):
    return reql.nth(value)


def offset(reql, value):
    return reql.offset(value)


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
    '$group': group,
    '$has_fields': has_fields,
    '$limit': limit,
    '$nth': nth,
    '$pluck': pluck,
    '$sample': sample,
    '$slice': slice,
    '$without': without,
}
