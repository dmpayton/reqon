import datetime
import geojson
import reqon
import rethinkdb as r
import unittest
import pytest

from reqon import coerce, terms
from .utils import ReQONTestMixin


class TermsTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_gather(self):
        assert sorted(terms.gather_terms().keys()) == sorted(terms.READ_TERMS.keys())
        assert '$delete' in terms.gather_terms(allow_delete=True).keys()

    # Get


    def test_get(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get'](self.reql, key='123'))
        reql2 = self.reqlify(lambda: self.reql.get('123'))
        assert str(reql1) == str(reql2)


    # Get All


    def test_get_all(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get_all'](self.reql, keys=['123', '456']))
        reql2 = self.reqlify(lambda: self.reql.get_all('123', '456', index='id'))
        assert str(reql1) == str(reql2)

    def test_get_all_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$get_all'](self.reql, keys=['123', '456'], index='rank'))
        reql2 = self.reqlify(lambda: self.reql.get_all('123', '456', index='rank'))
        assert str(reql1) == str(reql2)


    # Filter


    def test_filter(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$filter'](self.reql, predicate=[
            ['rank', ['$gt', 8]],
            ['age', ['$lt', 6]]
        ]))
        reql2 = self.reqlify(lambda: self.reql.filter(r.row['rank'].gt(8), default=False).filter(r.row['age'].lt(6), default=False))
        assert str(reql1) == str(reql2)


    def test_invalid_filter(self):
        with pytest.raises(reqon.exceptions.ReqonError):
            reqon.TERMS['$filter'](self.reql, predicate=[{'foo': 'bar'}])


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
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, index='title'))
        reql2 = self.reqlify(lambda: self.reql.order_by(index='title'))
        assert str(reql1) == str(reql2)

    def test_order_by_ascending(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, 'rank', ordering='$asc'))
        reql2 = self.reqlify(lambda: self.reql.order_by(r.asc('rank')))
        assert str(reql1) == str(reql2)

    def test_order_by_descending(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, 'rank', ordering='$desc'))
        reql2 = self.reqlify(lambda: self.reql.order_by(r.desc('rank')))
        assert str(reql1) == str(reql2)

    def test_order_by_asc_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, index='rank', ordering='$asc'))
        reql2 = self.reqlify(lambda: self.reql.order_by(index=r.asc('rank')))
        assert str(reql1) == str(reql2)

    def test_order_by_desc_indexed(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$order_by'](self.reql, index='rank', ordering='$desc'))
        reql2 = self.reqlify(lambda: self.reql.order_by(index=r.desc('rank')))
        assert str(reql1) == str(reql2)


    # Skip


    def test_skip(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$skip'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.skip(100))
        assert str(reql1) == str(reql2)


    # Limit


    def test_limit(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$limit'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.limit(100))
        assert str(reql1) == str(reql2)

    # Slice


    def test_slice(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$slice'](self.reql, 10, 20))
        reql2 = self.reqlify(lambda: self.reql.slice(10, 20))
        assert str(reql1) == str(reql2)


    # Nth


    def test_nth(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$nth'](self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.nth(100))
        assert str(reql1) == str(reql2)

    # Sample


    def test_sample(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$sample'](self.reql, 10))
        reql2 = self.reqlify(lambda: self.reql.sample(10))
        assert str(reql1) == str(reql2)


    # Pluck


    def test_pluck(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$pluck'](self.reql, ['title', 'year']))
        reql2 = self.reqlify(lambda: self.reql.pluck('title', 'year'))
        assert str(reql1) == str(reql2)


    # Without


    def test_without(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$without'](self.reql, ['title', 'year']))
        reql2 = self.reqlify(lambda: self.reql.without('title', 'year'))
        assert str(reql1) == str(reql2)


    # Group


    def test_group_field(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$group'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.group('rating', multi=False))
        assert str(reql1) == str(reql2)

    def test_group_index(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$group'](self.reql, index='rating'))
        reql2 = self.reqlify(lambda: self.reql.group(index='rating', multi=False))
        assert str(reql1) == str(reql2)


    # Count


    def test_count(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$count'](self.reql))
        reql2 = self.reqlify(lambda: self.reql.count())
        assert str(reql1) == str(reql2)


    # Sum


    def test_sum(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$sum'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.sum('rating'))
        assert str(reql1) == str(reql2)


    # Avg


    def test_avg(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$avg'](self.reql, field='rating'))
        reql2 = self.reqlify(lambda: self.reql.avg('rating'))
        assert str(reql1) == str(reql2)


    # Min


    def test_min(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$min'](self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.min('rating'))
        assert str(reql1) == str(reql2)


    # Max


    def test_max(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$max'](self.reql, field='rating'))
        reql2 = self.reqlify(lambda: self.reql.max('rating'))
        assert str(reql1) == str(reql2)


    # Between


    def test_between(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$between'](self.reql, '2016-01-01', '2016-01-31'))
        reql2 = self.reqlify(lambda: self.reql.between('2016-01-01', '2016-01-31'))
        assert str(reql1) == str(reql2)

    def test_between_kwargs(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$between'](self.reql, '2016-01-01', '2016-01-31', index='timestamp'))
        reql2 = self.reqlify(lambda: self.reql.between('2016-01-01', '2016-01-31', index='timestamp'))
        assert str(reql1) == str(reql2)

    def test_between_coerce(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$between'](self.reql,
            ['$date', '2016-01-01'], ['$date', '2016-01-31']))
        reql2 = self.reqlify(lambda: self.reql.between(coerce.coerce_date('2016-01-01'), coerce.coerce_date('2016-01-31')))
        assert str(reql1) == str(reql2)


    # Geo

    def test_get_intersecting(self):
        point = geojson.utils.generate_random('Point')
        reql1 = self.reqlify(lambda: reqon.TERMS['$get_intersecting'](self.reql, geometry=point, index='location'))
        reql2 = self.reqlify(lambda: self.reql.get_intersecting(r.point(*point['coordinates']), index='location'))
        assert str(reql1) == str(reql2)

    def test_get_nearest(self):
        point = geojson.utils.generate_random('Point')
        reql1 = self.reqlify(lambda: reqon.TERMS['$get_nearest'](self.reql, geometry=point, index='location'))
        reql2 = self.reqlify(lambda: self.reql.get_nearest(r.point(*point['coordinates']), index='location'))
        assert str(reql1) == str(reql2)


    # Delete

    def test_delete(self):
        reql1 = self.reqlify(lambda: reqon.TERMS['$delete'](self.reql))
        reql2 = self.reqlify(lambda: self.reql.delete(durability='hard', return_changes=False))
        assert str(reql1) == str(reql2)
