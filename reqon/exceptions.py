

class ReqonError(Exception):
    def __init__(self, message):
        self.message = message


class FilterError(ReqonError):
    pass


class ValidationError(ReqonError):
    pass
