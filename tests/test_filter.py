import geojson
import reqon
import rethinkdb as r
import unittest

from .utils import ReQONTestMixin


class FilterFunctionTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_ieq(self):
        reql1 = self.reqlify(lambda: reqon.filter.ieq(r.row['title'], 'star wars'))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('(?i)^star wars$'))
        assert str(reql1) == str(reql2)

    def test_in(self):
        reql1 = self.reqlify(lambda: reqon.filter.in_(r.row['rank'], [1, 2, 3]))
        reql2 = self.reqlify(lambda: r.expr([1, 2, 3]).contains(r.row['rank']))
        assert str(reql1) == str(reql2)

    def test_regex(self):
        reql1 = self.reqlify(lambda: reqon.filter.regex(r.row['title'], '(?i)^star '))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('(?i)^star '))
        assert str(reql1) == str(reql2)

    def test_starts(self):
        reql1 = self.reqlify(lambda: reqon.filter.starts(r.row['title'], 'star '))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('^star '))
        assert str(reql1) == str(reql2)

    def test_istarts(self):
        reql1 = self.reqlify(lambda: reqon.filter.istarts(r.row['title'], 'star '))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('(?i)^star '))
        assert str(reql1) == str(reql2)

    def test_ends(self):
        reql1 = self.reqlify(lambda: reqon.filter.ends(r.row['title'], ' wars'))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match(' wars$'))
        assert str(reql1) == str(reql2)

    def test_iends(self):
        reql1 = self.reqlify(lambda: reqon.filter.iends(r.row['title'], ' wars'))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('(?i) wars$'))
        assert str(reql1) == str(reql2)

    def test_intersects(self):
        polygon = geojson.utils.generate_random('Polygon')
        reql1 = self.reqlify(lambda: reqon.filter.intersects(r.row['location'], dict(polygon)))
        reql2 = self.reqlify(lambda: r.row['location'].intersects(r.polygon(*polygon['coordinates'])))
        assert str(reql1) == str(reql2)

    def test_includes(self):
        point = geojson.utils.generate_random('Point')
        reql1 = self.reqlify(lambda: reqon.filter.includes(r.row['location'], dict(point)))
        reql2 = self.reqlify(lambda: r.row['location'].includes(r.point(point['coordinates'])))
        assert str(reql1) == str(reql2)
