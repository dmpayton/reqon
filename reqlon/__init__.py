from . import geo, filter, terms


def query(reql, query):
    for sequence in query:
        term = sequence[0]
        reql = terms[term](reql, *sequence[1:])
