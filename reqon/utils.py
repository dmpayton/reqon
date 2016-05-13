import six


def expand_path(path):
    ''' Break a dot-notated path into a dict '''

    if isinstance(path, six.string_types):
        path = path.split('.')
        num_fields = len(path)
        if num_fields == 1:
            return path[0]
        row = node = {}
        for idx, field in enumerate(path):
            if idx + 1 == num_fields:
                node[field] = True
            else:
                node[field] = {}
                node = node[field]
        return row
    return path
