class TypeError(Exception):
    def __init__(self, message):
        super(TypeError, self).__init__(message)

class InvalidFilterError(Exception):
    def __init__(self, message):
        super(InvalidFilterError, self).__init__(message)
