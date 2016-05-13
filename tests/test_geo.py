import geojson
import pytest
import reqon
import rethinkdb as r
import unittest

from .utils import ReQONTestMixin


class GeoJSONToReQLTests(ReQONTestMixin, unittest.TestCase):
    def test_point(self):
        point = geojson.utils.generate_random('Point')
        reql1 = reqon.geo.geojson_to_reql(point)
        reql2 = r.point(*point['coordinates'])
        assert str(reql1) == str(reql2)

    def test_line(self):
        line = geojson.utils.generate_random('LineString')
        reql1 = reqon.geo.geojson_to_reql(line)
        reql2 = r.line(*line['coordinates'])
        assert str(reql1) == str(reql2)

    def test_polygon(self):
        polygon = geojson.utils.generate_random('Polygon')
        reql1 = reqon.geo.geojson_to_reql(polygon)
        reql2 = r.polygon(*polygon['coordinates'][0])
        assert str(reql1) == str(reql2)

    def test_circle(self):
        coordinates = geojson.utils.generate_random('Point')['coordinates']
        circle = reqon.geo.Circle(coordinates, radius=420)
        reql1 = reqon.geo.geojson_to_reql(circle)
        reql2 = r.circle(coordinates, radius=circle['radius'])
        assert str(reql1) == str(reql2)

    def test_circle_invalid_coordinates(self):
        coords = geojson.utils.generate_random('Point')['coordinates']
        circle = reqon.geo.Circle(coordinates=[coords], radius=0)
        output = reqon.geo.is_valid(circle)
        assert output['valid'] == 'no'
        assert '"coordinates"' in output['message']

    def test_circle_invalid_radius(self):
        coords = geojson.utils.generate_random('Point')['coordinates']
        circle = reqon.geo.Circle(coordinates=coords, radius='12km')
        output = reqon.geo.is_valid(circle)
        assert output['valid'] == 'no'
        assert '"radius"' in output['message']

    def test_geojson_to_reql_invalid(self):
        point = geojson.utils.generate_random('Point')
        point['coordinates'] = [point['coordinates']]
        with pytest.raises(reqon.exceptions.ValidationError):
            reqon.geo.geojson_to_reql(point)
