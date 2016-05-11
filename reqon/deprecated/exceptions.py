class ReqonError(Exception):
    pass

class InvalidTypeError(ReqonError):
    def __init__(self, message):
        super(InvalidTypeError, self).__init__(message)

class InvalidFilterError(ReqonError):
    def __init__(self, message):
        super(InvalidFilterError, self).__init__(message)
