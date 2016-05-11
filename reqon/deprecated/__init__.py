import rethinkdb as r

from . import coerce, geo, operators, terms
from .coerce import COERSIONS
from .operators import BOOLEAN, EXPRESSIONS, MODIFIERS
from .terms import TERMS
from .exceptions import ReqonError, InvalidTypeError, InvalidFilterError


def query(query):
    try:
        reql = r.db(query['$db']).table(query['$table'])
    except KeyError:
        try:
            reql = r.table(query['$table'])
        except KeyError:
            raise ReqonError('The query descriptor requires a $table key.')

    for sequence in query['$query']:
        term = sequence[0]
        try:
            reql = TERMS[term](reql, *sequence[1:])
        except ReqonError:
            raise
        except r.ReqlError:
            message = 'Invalid values for {0} with args {1}'
            raise ReqonError(message.format(term, sequence[1:]))
        except Exception:
            message = 'Unknown exception, {0}: {1}'
            raise ReqonError(message.format(term, sequence[1:]))

    return reql
