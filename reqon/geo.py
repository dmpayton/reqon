import geojson
import json
import rethinkdb as r
import six

from .exceptions import ValidationError


class Point(geojson.Point):
    def as_reql(self):
        return r.point(*self['coordinates'])


class LineString(geojson.LineString):
    def as_reql(self):
        return r.line(*self['coordinates'])


class Polygon(geojson.Polygon):
    def as_reql(self):
        return r.polygon(*self['coordinates'][0])


class Circle(geojson.geometry.Geometry):
    _optional = (
        'num_vertices',
        'geo_system',
        'unit',
        'fill',
    )

    def __init__(self, coordinates, radius, **kwargs):
        kwargs = {key: kwargs[key] for key in self._optional if key in kwargs}
        super(Circle, self).__init__(coordinates, radius=radius, **kwargs)

    def as_reql(self):
        kwargs = {key: self[key] for key in self._optional if key in self}
        return r.circle(self['coordinates'], radius=self['radius'], **kwargs)


SHAPES = {
    'Point': Point,
    'LineString': LineString,
    'Polygon': Polygon,
    'Circle': Circle,
}


def is_valid(obj):
    output = geojson.validation.output
    if isinstance(obj, Circle):
        if len(obj.coordinates) != 2:
            return output('the "coordinates" member must be a single position')
        if obj.radius is None or not isinstance(obj['radius'], (int, float)):
            return output('the "radius" member must be an integer')
        return output('')
    return geojson.is_valid(obj)


def geojson_to_reql(data):
    from .validators import validate_geojson

    # Geometry might be passed as a JSON string
    if isinstance(data, six.string_types):
        data = json.loads(data)

    data = validate_geojson(data)
    geometry = SHAPES[data['type']](**data)
    output = is_valid(geometry)
    if output['valid'] == 'no':
        raise ValidationError(output['message'])

    return geometry.as_reql()
