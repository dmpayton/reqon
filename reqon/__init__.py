import rethinkdb as r

from . import geo, operators, terms
from .operators import BOOLEAN, EXPRESSIONS
from .terms import TERMS


def query(query):
    try:
        reql = r.db(query['$db']).table(query['$table'])
    except KeyError:
        try:
            reql = r.table(query['$table'])
        except KeyError:
            raise

    for sequence in query['$query']:
        term = sequence[0]
        reql = TERMS[term](reql, *sequence[1:])

    return reql
