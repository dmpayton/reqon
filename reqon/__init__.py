import rethinkdb as r

from . import coerce, exceptions, geo, operators, terms
from .coerce import COERSIONS
from .operators import BOOLEAN, EXPRESSIONS, MODIFIERS
from .terms import TERMS
from .validators import validate_query


def build_reql(query):
    query = validate_query(query)

    try:
        reql = r.db(query['$db']).table(query['$table'])
    except KeyError:
        reql = r.table(query['$table'])

    for sequence in query.get('$query', []):
        try:
            term, kwargs = sequence
        except ValueError:
            # Not all terms take kwargs, so use an empty dict
            term, kwargs = sequence[0], {}

        try:
            reql = TERMS[term](reql, **kwargs)
        except ReqonError as err:
            # Re-raise, but prepend with the term
            raise ReqonError('{0}: {1}'.join(term, ''.join(err.args)))
        except r.ReqlError:
            message = 'Invalid values: {0}({1})'
            raise ReqonError(message.format(term, kwargs))
        except Exception:
            message = 'Unknown error: {0}({1})'
            raise ReqonError(message.format(term, kwargs))

    return reql
