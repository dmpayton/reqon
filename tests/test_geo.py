import geojson
import reqon
import rethinkdb as r
import unittest


class GeoTests(unittest.TestCase):
    def test_point(self):
        point = geojson.utils.generate_random('Point')
        reql1 = reqon.geo.geojson_to_reql(point)
        reql2 = r.point(point['coordinates'])
        assert str(reql1) == str(reql2)

    def test_line(self):
        line = geojson.utils.generate_random('LineString')
        reql1 = reqon.geo.geojson_to_reql(line)
        reql2 = r.line(*line['coordinates'])
        assert str(reql1) == str(reql2)

    def test_polygon(self):
        polygon = geojson.utils.generate_random('Polygon')
        reql1 = reqon.geo.geojson_to_reql(polygon)
        reql2 = r.polygon(*polygon['coordinates'])
        assert str(reql1) == str(reql2)

    def test_circle(self):
        point = geojson.utils.generate_random('Point')
        circle = reqon.geo.Circle(point['coordinates'], radius=420)
        reql1 = reqon.geo.geojson_to_reql(circle)
        reql2 = r.circle(point['coordinates'], radius=circle['radius'])
        assert str(reql1) == str(reql2)
