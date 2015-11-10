import geojson
import rethinkdb as r


class Circle(geojson.geometry.Geometry):
    def __init__(self, coordinates, radius=0, **kwargs):
        super(Circle, self).__init__(coordinates, radius=radius, **kwargs)


GEO_TYPES = {
    'Point': (geojson.Point, lambda geo: r.point(*geo['coordinates'])),
    'LineString': (geojson.LineString, lambda geo: r.line(*geo['coordinates'])),
    'Polygon': (geojson.Polygon, lambda geo: r.polygon(*geo['coordinates'][0])),
    'Circle': (Circle, lambda geo: r.circle(geo['coordinates'], radius=geo['radius'])),
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
    GeoShape, reql_shape = GEO_TYPES[data.pop('type')]
    geometry = GeoShape(**data)
    output = is_valid(geometry)
    if output['valid'] == 'no':
        raise ValueError(output['message'])
    return reql_shape(data)
