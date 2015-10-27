import rethinkdb as r

from . import geo, filter, terms


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
        reql = terms.TERMS[term](reql, *sequence[1:])

    return reql
