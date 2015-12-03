class TypeError(Exception):
    def __init__(self, message):
        super(TypeError, self).__init__(message)

class InvalidExpressionError(Exception):
    def __init__(self, message):
        super(InvalidExpressionError, self).__init__(message)
