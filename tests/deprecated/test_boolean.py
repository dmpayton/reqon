import geojson
import reqon.deprecated as reqon
import rethinkdb as r
import unittest

from .utils import ReQONTestMixin


class FilterFunctionTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_and(self):
        reql1 = self.reqlify(lambda: reqon.operators.build(['$and', [
            ['year', 1987],
            ['rank', ['$gt', 8]]
        ]]))
        reql2 = self.reqlify(lambda: r.and_(
            r.row['year'].eq(1987),
            r.row['rank'].gt(8)
        ))
        assert str(reql1) == str(reql2)

    def test_or(self):
        reql1 = self.reqlify(lambda: reqon.operators.build(['$or', [
            ['year', ['$gt', 1999]],
            ['year', ['$lt', 1990]]
        ]]))
        reql2 = self.reqlify(lambda: r.or_(
            r.row['year'].gt(1999),
            r.row['year'].lt(1990)
        ))
        assert str(reql1) == str(reql2)

    def test_nested(self):
        reql1 = self.reqlify(lambda: reqon.operators.build(['$and', [
            ['rank', ['$gt', 8]],
            ['$or', [
                ['year', ['$gt', 1999]],
                ['year', ['$lt', 1990]]
            ]]
        ]]))
        reql2 = self.reqlify(lambda: r.and_(
            r.row['rank'].gt(8),
            r.or_(
                r.row['year'].gt(1999),
                r.row['year'].lt(1990)
            )
        ))
        assert str(reql1) == str(reql2)

    def test_not(self):
        reql1 = self.reqlify(lambda: reqon.operators.build(['$not',
            ['year', ['$lt', 1990]],
        ]))
        reql2 = self.reqlify(lambda: r.not_(
            r.row['year'].lt(1990)
        ))
        assert str(reql1) == str(reql2)
