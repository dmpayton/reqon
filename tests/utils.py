import rethinkdb as r


class ReQONTestMixin(object):
    def reqlify(self, func):
        '''Reset the nextVarId before running a func that is expected to return ReQL.'''
        r.ast.Func.nextVarId = 1
        return func()
