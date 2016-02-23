import datetime
import geojson
import reqon
import rethinkdb as r
import unittest

from .utils import ReQONTestMixin


class FilterFunctionTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_ieq(self):
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$ieq'](r.row['title'], 'star wars'))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('(?i)^star wars$'))
        assert str(reql1) == str(reql2)

    def test_in(self):
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$in'](r.row['rank'], [1, 2, 3]))(r.row)
        reql2 = self.reqlify(lambda: (lambda doc: r.expr([1, 2, 3]).contains(doc['rank']))(r.row))
        assert str(reql1) == str(reql2)

    def test_regex(self):
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$regex'](r.row['title'], '(?i)^star '))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('(?i)^star '))
        assert str(reql1) == str(reql2)

    def test_starts(self):
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$starts'](r.row['title'], 'star '))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('^star '))
        assert str(reql1) == str(reql2)

    def test_istarts(self):
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$istarts'](r.row['title'], 'star '))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('(?i)^star '))
        assert str(reql1) == str(reql2)

    def test_ends(self):
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$ends'](r.row['title'], ' wars'))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match(' wars$'))
        assert str(reql1) == str(reql2)

    def test_iends(self):
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$iends'](r.row['title'], ' wars'))
        reql2 = self.reqlify(lambda: r.row['title'].coerce_to('string').match('(?i) wars$'))
        assert str(reql1) == str(reql2)

    def test_intersects(self):
        polygon = geojson.utils.generate_random('Polygon')
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$intersects'](r.row['location'], dict(polygon)))
        reql2 = self.reqlify(lambda: r.row['location'].intersects(r.polygon(*polygon['coordinates'][0])))
        assert str(reql1) == str(reql2)

    def test_includes(self):
        point = geojson.utils.generate_random('Point')
        reql1 = self.reqlify(lambda: reqon.EXPRESSIONS['$includes'](r.row['location'], dict(point)))
        reql2 = self.reqlify(lambda: r.row['location'].includes(r.point(*point['coordinates'])))
        assert str(reql1) == str(reql2)

    def test_modifiers(self):
        # ['birthday.$date', ['$eq', ['$date', '1987-07-24']]]
        reql1 = self.reqlify(lambda: reqon.MODIFIERS['$date'](r.row['birthday']))
        reql2 = self.reqlify(lambda: r.row['birthday'].date())
        assert str(reql1) == str(reql2)


    def test_date_modifier(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$filter'](self.reql, [
            ['birthday', ['$date', '1987-07-24']]
        ]))
        #reql2 = self.reqlify(lambda: self.reql.filter(r.and_(r.row['birthday'].date().eq(datetime.date(2987, 7, 24)))))
        #assert str(reql1) == str(reql2)
