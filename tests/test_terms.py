import reqon
import rethinkdb as r
import unittest
import pytest

from reqon import terms
from .utils import ReQONTestMixin


class TermsTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    # Expand Path


    def test_expand_path(self):
        expanded = terms._expand_path('foo.bar.baz')
        expected = {'foo': { 'bar': { 'baz': True } } }
        assert expected == expanded

    def test_expand_path_invalid_type(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms._expand_path(1)
        assert terms.ERRORS['type']['string'].format('expand_path') == str(excinfo.value)


    # Get


    def test_get(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get'](self.reql, '123'))
        reql2 = self.reqlify(lambda: self.reql.get('123'))
        assert str(reql1) == str(reql2)

    def test_get_invalid_type(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.get(self.reql, { "foo": "bar" })
        assert terms.ERRORS['type']['invalid'].format('get') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.get(self.reql, [1, 2, {"foo": "bar"}])
        assert terms.ERRORS['type']['invalid'].format('get') == str(excinfo.value)


    # Get All


    def test_get_all(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get_all'](self.reql, ['123', '456']))
        reql2 = self.reqlify(lambda: self.reql.get_all('123', '456', index='id'))
        assert str(reql1) == str(reql2)

    def test_get_all_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get_all'](self.reql, ['rank', ['123', '456']]))
        reql2 = self.reqlify(lambda: self.reql.get_all('123', '456', index='rank'))
        assert str(reql1) == str(reql2)


    # Filter


    def test_filter(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$filter'](self.reql, [
            ['rank', ['$gt', 8]],
            ['age', ['$lt', 6]]
        ]))
        reql2 = self.reqlify(lambda: self.reql.filter(r.and_(r.row['rank'].gt(8), r.row['age'].lt(6))))
        assert str(reql1) == str(reql2)


    def test_invalid_filter(self):
        with pytest.raises(reqon.exceptions.InvalidFilterError) as excinfo:
            terms.filter_(self.reql, [{ 'foo': 'bar' }])
        assert terms.ERRORS['filter']['invalid'].format("[{'foo': 'bar'}]") == str(excinfo.value)


    # Has Fields


    def test_has_fields(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$has_fields'](self.reql, ['title']))
        reql2 = self.reqlify(lambda: self.reql.has_fields('title'))
        assert str(reql1) == str(reql2)


    # With Fields


    def test_with_fields(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$with_fields'](self.reql, ['title']))
        reql2 = self.reqlify(lambda: self.reql.with_fields('title'))
        assert str(reql1) == str(reql2)


    # Order By


    def test_order_by(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, 'title'))
        reql2 = self.reqlify(lambda: self.reql.order_by('title'))
        assert str(reql1) == str(reql2)

    def test_order_by_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, ['$index', 'title']))
        reql2 = self.reqlify(lambda: self.reql.order_by(index='title'))
        assert str(reql1) == str(reql2)


    # Skip


    def test_skip(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$skip'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.skip(100))
        assert str(reql1) == str(reql2)

    def test_invalid_skip(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.skip(self.reql, "4")
        assert terms.ERRORS['type']['int'].format('skip') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.skip(self.reql, 1.4)
        assert terms.ERRORS['type']['int'].format('skip') == str(excinfo.value)


    # Limit


    def test_limit(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$limit'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.limit(100))
        assert str(reql1) == str(reql2)

    def test_invalid_limit(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.limit(self.reql, "10")
        assert terms.ERRORS['type']['int'].format('limit') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.limit(self.reql, 10.5)
        assert terms.ERRORS['type']['int'].format('limit') == str(excinfo.value)

    # Slice


    def test_slice(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$slice'](self.reql, [10, 20]))
        reql2 = self.reqlify(lambda: self.reql.slice(10, 20))
        assert str(reql1) == str(reql2)

    def test_invalid_slice(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.slice_(self.reql, 10)
        assert terms.ERRORS['type']['invalid'].format('slice') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.slice_(self.reql, [10.4, 10])
        assert terms.ERRORS['type']['invalid'].format('slice') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.slice_(self.reql, ["10", 20])
        assert terms.ERRORS['type']['invalid'].format('slice') == str(excinfo.value)


    # Nth


    def test_nth(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$nth'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.nth(100))
        assert str(reql1) == str(reql2)

    def test_invalid_nth(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.nth(self.reql, "10")
        assert terms.ERRORS['type']['int'].format('nth') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.nth(self.reql, 10.5)
        assert terms.ERRORS['type']['int'].format('nth') == str(excinfo.value)

    # Sample


    def test_sample(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$sample'](self.reql, 10))
        reql2 = self.reqlify(lambda: self.reql.sample(10))
        assert str(reql1) == str(reql2)

    def test_invalid_sample(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.sample(self.reql, "10")
        assert terms.ERRORS['type']['int'].format('sample') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.sample(self.reql, 10.5)
        assert terms.ERRORS['type']['int'].format('sample') == str(excinfo.value)


    # Pluck


    def test_pluck(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$pluck'](self.reql, ['title', 'year']))
        reql2 = self.reqlify(lambda: self.reql.pluck('title', 'year'))
        assert str(reql1) == str(reql2)

    def test_invalid_pluck(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.pluck(self.reql, "10")
        assert terms.ERRORS['type']['invalid'].format('pluck') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.pluck(self.reql, ["10", 1])
        assert terms.ERRORS['type']['invalid'].format('pluck') == str(excinfo.value)


    # Without


    def test_without(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$without'](self.reql, ['title', 'year']))
        reql2 = self.reqlify(lambda: self.reql.without('title', 'year'))
        assert str(reql1) == str(reql2)

    def test_invalid_without(self):
        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.without(self.reql, "10")
        assert terms.ERRORS['type']['invalid'].format('without') == str(excinfo.value)

        with pytest.raises(reqon.exceptions.TypeError) as excinfo:
            terms.without(self.reql, ["10", 1])
        assert terms.ERRORS['type']['invalid'].format('without') == str(excinfo.value)

    # Group


    def test_group(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$group'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.group('rating'))
        assert str(reql1) == str(reql2)

    def test_group_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$group'](self.reql, ['$index', 'rating']))
        reql2 = self.reqlify(lambda: self.reql.group(index='rating'))
        assert str(reql1) == str(reql2)


    # Count


    def test_count(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$count'](self.reql))
        reql2 = self.reqlify(lambda: self.reql.count())
        assert str(reql1) == str(reql2)

    def test_count_field(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$count'](self.reql, 'year'))
        reql2 = self.reqlify(lambda: self.reql.count('year'))
        assert str(reql1) == str(reql2)


    # Sum


    def test_sum(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$sum'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.sum('rating'))
        assert str(reql1) == str(reql2)


    # Avg


    def test_avg(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$avg'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.avg('rating'))
        assert str(reql1) == str(reql2)


    # Min


    def test_min(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$min'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.min('rating'))
        assert str(reql1) == str(reql2)


    # Max


    def test_max(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$max'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.max('rating'))
        assert str(reql1) == str(reql2)
