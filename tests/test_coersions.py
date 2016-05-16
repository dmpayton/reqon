import datetime
import geojson
import pytz
import reqon
import rethinkdb as r
import unittest

from .utils import ReQONTestMixin


class GeoJSONToReQLTests(ReQONTestMixin, unittest.TestCase):
    def test_none(self):
        value = 'no coersion necessary'
        assert reqon.coerce.coerce(value) == value

    def test_datetime(self):
        dt1 = reqon.coerce.coerce(['$datetime', '1987-07-24 9:07pm'])
        dt2 = datetime.datetime(1987, 7, 24, 21, 7, tzinfo=pytz.utc)
        assert dt1 == dt2

    def test_date(self):
        dt1 = reqon.coerce.coerce(['$date', '1987-07-24 9:07pm'])
        dt2 = datetime.datetime(1987, 7, 24, tzinfo=pytz.utc)
        assert dt1 == dt2

    def test_time(self):
        dt1 = reqon.coerce.coerce(['$time', '4:20pm'])
        dt2 = datetime.time(16, 20)
        assert dt1 == dt2

    def test_minval(self):
        coerced = reqon.coerce.coerce('$minval')
        assert coerced == r.minval

    def test_maxval(self):
        coerced = reqon.coerce.coerce('$maxval')
        assert coerced == r.maxval

    def test_point(self):
        point = geojson.utils.generate_random('Point')
        point1 = reqon.coerce.coerce(['$geojson', dict(point)])
        point2 = reqon.coerce.coerce(['$geojson', geojson.dumps(point)])
        point3 = r.point(*point['coordinates'])
        assert point1 == point2 == point3

    def test_line(self):
        line = geojson.utils.generate_random('LineString')
        line1 = reqon.coerce.coerce(['$geojson', dict(line)])
        line2 = reqon.coerce.coerce(['$geojson', geojson.dumps(line)])
        line3 = r.line(*line['coordinates'])
        assert line1 == line2 == line3

    def test_polygon(self):
        poly = geojson.utils.generate_random('Polygon')
        poly1 = reqon.coerce.coerce(['$geojson', dict(poly)])
        poly2 = reqon.coerce.coerce(['$geojson', geojson.dumps(poly)])
        poly3 = r.polygon(*poly['coordinates'])
        assert poly1 == poly2 == poly3
