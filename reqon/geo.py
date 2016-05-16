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


GEOMETRIES = {
    'Point': Point,
    'LineString': LineString,
    'Polygon': Polygon,
    'Circle': Circle,
}


def geojson_to_reql(data):
    from .validators import validate_geojson

    # Geometry might be passed as a JSON string
    if isinstance(data, six.string_types):
        data = json.loads(data)

    data = validate_geojson(data)
    geometry = GEOMETRIES[data['type']](**data)
    return geometry.as_reql()
