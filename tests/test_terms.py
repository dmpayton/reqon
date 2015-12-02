import reqon
import rethinkdb as r
import unittest
import pytest

from reqon import terms
from .utils import ReQONTestMixin


class TermsTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_expand_path(self):
        expanded = terms.expand_path('foo.bar.baz')
        expected = {'foo': { 'bar': { 'baz': True } } }
        assert expected == expanded

    def test_expand_path_invalid_type(self):
        with pytest.raises(TypeError) as excinfo:
            terms.expand_path(1)
        assert 'Invalid type passed to expand_path. Must be a String', excinfo.value
        
    def test_get(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get'](self.reql, '123'))
        reql2 = self.reqlify(lambda: self.reql.get('123'))
        assert str(reql1) == str(reql2)

    def test_get_all(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get_all'](self.reql, ['123', '456']))
        reql2 = self.reqlify(lambda: self.reql.get_all('123', '456', index='id'))
        assert str(reql1) == str(reql2)

    def test_get_all_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get_all'](self.reql, ['rank', ['123', '456']]))
        reql2 = self.reqlify(lambda: self.reql.get_all('123', '456', index='rank'))
        assert str(reql1) == str(reql2)

    def test_filter(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$filter'](self.reql, [
            ['rank', ['$gt', 8]]
        ]))
        reql2 = self.reqlify(lambda: self.reql.filter(r.and_(r.row['rank'].gt(8))))
        assert str(reql1) == str(reql2)

    def test_has_fields(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$has_fields'](self.reql, ['title']))
        reql2 = self.reqlify(lambda: self.reql.has_fields('title'))
        assert str(reql1) == str(reql2)

    def test_with_fields(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$with_fields'](self.reql, ['title']))
        reql2 = self.reqlify(lambda: self.reql.with_fields('title'))
        assert str(reql1) == str(reql2)

    def test_order_by(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, 'title'))
        reql2 = self.reqlify(lambda: self.reql.order_by('title'))
        assert str(reql1) == str(reql2)

    def test_order_by_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, ['$index', 'title']))
        reql2 = self.reqlify(lambda: self.reql.order_by(index='title'))
        assert str(reql1) == str(reql2)

    def test_skip(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$skip'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.skip(100))
        assert str(reql1) == str(reql2)

    def test_limit(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$limit'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.limit(100))
        assert str(reql1) == str(reql2)

    def test_slice(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$slice'](self.reql, [10, 20]))
        reql2 = self.reqlify(lambda: self.reql.slice(10, 20))
        assert str(reql1) == str(reql2)

    def test_nth(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$nth'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.nth(100))
        assert str(reql1) == str(reql2)

    def test_sample(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$sample'](self.reql, 10))
        reql2 = self.reqlify(lambda: self.reql.sample(10))
        assert str(reql1) == str(reql2)

    def test_pluck(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$pluck'](self.reql, ['title', 'year']))
        reql2 = self.reqlify(lambda: self.reql.pluck('title', 'year'))
        assert str(reql1) == str(reql2)

    def test_without(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$without'](self.reql, ['title', 'year']))
        reql2 = self.reqlify(lambda: self.reql.without('title', 'year'))
        assert str(reql1) == str(reql2)

    def test_group(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$group'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.group('rating'))
        assert str(reql1) == str(reql2)

    def test_group_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$group'](self.reql, ['$index', 'rating']))
        reql2 = self.reqlify(lambda: self.reql.group(index='rating'))
        assert str(reql1) == str(reql2)

    def test_count(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$count'](self.reql))
        reql2 = self.reqlify(lambda: self.reql.count())
        assert str(reql1) == str(reql2)

    def test_count_field(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$count'](self.reql, 'year'))
        reql2 = self.reqlify(lambda: self.reql.count('year'))
        assert str(reql1) == str(reql2)

    def test_sum(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$sum'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.sum('rating'))
        assert str(reql1) == str(reql2)

    def test_avg(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$avg'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.avg('rating'))
        assert str(reql1) == str(reql2)

    def test_min(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$min'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.min('rating'))
        assert str(reql1) == str(reql2)

    def test_max(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$max'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.max('rating'))
        assert str(reql1) == str(reql2)
