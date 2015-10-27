import rethinkdb as r


class ReQONTestMixin(object):
    def reqlify(self, func):
        # Reset the nextVarId before running a func that is expected
        # to return ReQL.

        # This is necessary because the rethinkdb library uses a global
        # counter for variables inside reql that makes it otherwise
        # impossible to directly compare two reql queries for equivalence
        # (whether by calling `reql.build()` or `str(reql)`).

        r.ast.Func.nextVarId = 1
        return func()
