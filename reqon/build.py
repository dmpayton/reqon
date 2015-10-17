import rethinkdb as r


def build(node):
    op, value = node
    if op in LOGIC_OPS:
        builder, func = LOGIC_OPS[op]
        return builder(value, func)
    return build_attribute(op, value)


def build_sequence(node, func):
    return func(*map(build, node))


def build_unary(node, func):
    return func(build(node))


def build_attribute(attrs, value):
    row = r.row
    for attr in attrs.split('.'):
        row = row[attr]

    func = r.eq  # equality by default
    if isinstance(value, list) and value[0] in BOOL_OPS:
        op, value = value
        func = BOOL_OPS[op]

    return func(row, value)
