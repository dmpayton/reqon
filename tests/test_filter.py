import geojson
import reqon
import rethinkdb as r
import unittest


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')


    # def test_eq(self):
    #     reql1 = reqon.filter.eq(r.row['title'], 'Star Wars')
    #     reql2 = r.eq(r.row['title'], 'Star Wars')
    #     assert reql1.build() == reql2.build()

    def test_ieq(self):
        reql1 = reqon.filter.ieq(r.row['title'], 'star wars')
        reql2 = r.row['title'].coerce_to('string').match('(?i)star wars')
        # assert reql1.build() == reql2.build()

    # def test_ne(self):
    #     reql1 = reqon.filter.ne(r.row['rank'], 1)
    #     reql2 = r.ne(r.row['rank'], 1)
    #     assert reql1.build() == reql2.build()

    # def test_gt(self):
    #     reql1 = reqon.filter.gt(r.row['rank'], 1)
    #     reql2 = r.gt(r.row['rank'], 1)
    #     assert reql1.build() == reql2.build()

    # def test_ge(self):
    #     reql1 = reqon.filter.ge(r.row['rank'], 1)
    #     reql2 = r.ge(r.row['rank'], 1)
    #     assert reql1.build() == reql2.build()

    # def test_lt(self):
    #     reql1 = reqon.filter.lt(r.row['rank'], 8)
    #     reql2 = r.lt(r.row['rank'], 8)
    #     assert reql1.build() == reql2.build()

    # def test_le(self):
    #     reql1 = reqon.filter.le(r.row['rank'], 1)
    #     reql2 = r.le(r.row['rank'], 1)
    #     assert reql1.build() == reql2.build()

    def test_in(self):
        reql1 = reqon.filter.in_(r.row['rank'], [1, 2, 3])
        reql2 = r.expr([1, 2, 3]).contains(r.row['rank'])
        # assert reql1.build() == reql2.build()

    def test_regex(self):
        reql1 = reqon.filter.regex(r.row['title'], '(?i)^star ')
        reql2 = r.row['title'].coerce_to('string').match('(?i)^star ')
        # assert reql1.build() == reql2.build()

    def test_starts(self):
        reql1 = reqon.filter.starts(r.row['title'], 'star ')
        reql2 = r.row['title'].coerce_to('string').match('^star ')
        # assert reql1.build() == reql2.build()

    def test_istarts(self):
        reql1 = reqon.filter.istarts(r.row['title'], 'star ')
        reql2 = r.row['title'].coerce_to('string').match('(?i)^star ')
        # assert reql1.build() == reql2.build()

    def test_ends(self):
        reql1 = reqon.filter.ends(r.row['title'], ' wars')
        reql2 = r.row['title'].coerce_to('string').match(' wars$')
        # assert reql1.build() == reql2.build()

    def test_iends(self):
        reql1 = reqon.filter.istarts(r.row['title'], ' wars')
        reql2 = r.row['title'].coerce_to('string').match('(?i) wars$')
        # assert reql1.build() == reql2.build()

    def test_intersects(self):
        polygon = geojson.utils.generate_random('Polygon')
        reql1 = reqon.filter.intersects(r.row['location'], dict(polygon))
        reql2 = r.row['location'].intersects(r.polygon(*polygon['coordinates']))
        # assert reql1.build() == reql2.build()

    def test_includes(self):
        point = geojson.utils.generate_random('Point')
        reql1 = reqon.filter.includes(r.row['location'], dict(point))
        reql2 = r.row['location'].intersects(r.point(point['coordinates']))
        # assert reql1.build() == reql2.build()
