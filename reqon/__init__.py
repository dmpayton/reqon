import rethinkdb as r

from . import coerce, exceptions, geo, operators, terms
from .coerce import COERSIONS
from .exceptions import ReqonError
from .operators import BOOLEAN, EXPRESSIONS, MODIFIERS
from .terms import gather_terms, TERMS
from .validators import validate_query


def build_reql(query, allow_delete=False):
    query = validate_query(query)

    try:
        reql = r.db(query['$db']).table(query['$table'])
    except KeyError:
        reql = r.table(query['$table'])

    return build_terms(reql, query.get('$query', []), allow_delete=allow_delete)


def build_terms(reql, query, allow_delete=False):
    terms = gather_terms(allow_delete=allow_delete)

    for sequence in query:
        try:
            term, kwargs = sequence
        except ValueError:
            # Not all terms take kwargs, so use an empty dict
            term, kwargs = sequence[0], {}

        try:
            reql = terms[term](reql, **kwargs)
        except ReqonError as err:
            # Re-raise, but prepend with the term
            raise ReqonError('{0}: {1}'.join(term, err.message))
        except r.ReqlError as err:
            message = '{0}: {1}'
            raise ReqonError(message.format(term, err.message))
        except Exception:
            message = '{0}: Unknown error'
            raise ReqonError(message.format(term, kwargs))

    return reql
