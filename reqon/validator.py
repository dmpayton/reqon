import jsonschema

from .exceptions import ValidationError
from .terms import TERMS


query_schema = jsonschema.Draft4Validator({
    'type': 'object',
    'properties': {
        '$db': {'type': 'string'},
        '$table': {'type': 'string'},
        '$query': {
            'type': 'array',
            'items': {
                'oneOf': [
                    { # Empty query
                        'type': 'array',
                        'minItems': 0,
                        'maxItems': 0
                    },
                    { # Term with no arguments
                        'type': 'array',
                        'items': [
                            {'enum': list(TERMS.keys())},
                        ],
                        'minItems': 1,
                        'maxItems': 1
                    },
                    { # Term with arguments
                        'type': 'array',
                        'items': [
                            {'enum': list(TERMS.keys())},
                            {'type': 'object'},
                        ],
                        'minItems': 2,
                        'maxItems': 2
                    }
                ]
            }
        }
    },
    'required': ['$table', '$query']
})


def schema_validator(schema):
    def validator(value):
        try:
            schema.validate(value)
        except jsonschema.ValidationError as err:
            raise ValidationError(err.message)
        return value
    return validator


validate = schema_validator(query_schema)