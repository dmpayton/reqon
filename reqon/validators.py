import jsonschema

from .exceptions import ValidationError
from .terms import TERMS

query_schema = jsonschema.Draft4Validator({
    '$schema': 'http://json-schema.org/draft-04/schema#',
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
    'required': ['$table']
}, types={'array': (list, tuple)})

# https://github.com/fge/sample-json-schemas/blob/master/geojson/geometry.json
geojson_schema = jsonschema.Draft4Validator({
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'title': 'Geometry',
    'description': 'One geometry as defined by GeoJSON',
    'type': 'object',
    'required': ['type', 'coordinates'],
    'oneOf': [
        {
            'title': 'Point',
            'properties': {
                'type': {'enum': ['Point']},
                'coordinates': {'$ref': '#/definitions/position'}
            }
        },
        # { # Not (yet) supported by RethinkDB
        #     'title': 'MultiPoint',
        #     'properties': {
        #         'type': {'enum': ['MultiPoint']},
        #         'coordinates': {'$ref': '#/definitions/positionArray'}
        #     }
        # },
        {
            'title': 'LineString',
            'properties': {
                'type': {'enum': ['LineString']},
                'coordinates': {'$ref': '#/definitions/lineString'}
            }
        },
        # { # Not (yet) supported by RethinkDB
        #     'title': 'MultiLineString',
        #     'properties': {
        #         'type': {'enum': ['MultiLineString']},
        #         'coordinates': {
        #             'type': 'array',
        #             'items': {'$ref': '#/definitions/lineString'}
        #         }
        #     }
        # },
        {
            'title': 'Polygon',
            'properties': {
                'type': {'enum': ['Polygon']},
                'coordinates': {'$ref': '#/definitions/polygon'}
            }
        },
        # { # Not (yet) supported by RethinkDB
        #     'title': 'MultiPolygon',
        #     'properties': {
        #         'type': {'enum': ['MultiPolygon']},
        #         'coordinates': {
        #             'type': 'array',
        #             'items': {'$ref': '#/definitions/polygon'}
        #         }
        #     }
        # }
        { # Custom implementation to convert a GeoJSON-esque data structure into r.circle
            'title': 'Circle',
            'properties': {
                'type': {'enum': ['Circle']},
                'coordinates': {'$ref': '#/definitions/position'},
                'radius': {'type': 'number'},
            },
            'additionalProperties': True
        },
    ],
    'definitions': {
        'position': {
            'description': 'A single position',
            'type': 'array',
            'minItems': 2,
            'items': [{'type': 'number'}, {'type': 'number'}],
            'additionalItems': False
        },
        'positionArray': {
            'description': 'An array of positions',
            'type': 'array',
            'items': {'$ref': '#/definitions/position'}
        },
        'lineString': {
            'description': 'An array of two or more positions',
            'allOf': [
                {'$ref': '#/definitions/positionArray'},
                {'minItems': 2}
            ]
        },
        'linearRing': {
            'description': 'An array of four positions where the first equals the last',
            'allOf': [
                {'$ref': '#/definitions/positionArray'},
                {'minItems': 4}
            ]
        },
        'polygon': {
            'description': 'An array of linear rings',
            'type': 'array',
            'items': {'$ref': '#/definitions/linearRing'}
        }
    }
}, types={'array': (list, tuple)})


def schema_validator(schema):
    def validator(value):
        try:
            schema.validate(value)
        except jsonschema.ValidationError as err:
            raise ValidationError(err.message)
        return value
    return validator


validate_query = schema_validator(query_schema)
validate_geojson = schema_validator(geojson_schema)
