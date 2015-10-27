import reqon
import rethinkdb as r
import unittest

from .utils import ReQONTestMixin


class TermsTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_get(self):
        reql1 = self.reqlify(lambda: reqon.terms.get(self.reql, '123'))
        reql2 = self.reqlify(lambda: self.reql.get('123'))
        assert str(reql1) == str(reql2)

    def test_get_all(self):
        reql1 = self.reqlify(lambda: reqon.terms.get_all(self.reql, ['123', '456']))
        reql2 = self.reqlify(lambda: self.reql.get_all('123', '456', index='id'))
        assert str(reql1) == str(reql2)

    def test_group(self):
        reql1 = self.reqlify(lambda: reqon.terms.group(self.reql, 'rating'))
        reql2 = self.reqlify(lambda: self.reql.group('rating'))
        assert str(reql1) == str(reql2)

    def test_has_fields(self):
        reql1 = self.reqlify(lambda: reqon.terms.has_fields(self.reql, ['title']))
        reql2 = self.reqlify(lambda: self.reql.has_fields('title'))
        assert str(reql1) == str(reql2)

    def test_limit(self):
        reql1 = self.reqlify(lambda: reqon.terms.limit(self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.limit(100))
        assert str(reql1) == str(reql2)

    def test_nth(self):
        reql1 = self.reqlify(lambda: reqon.terms.nth(self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.nth(100))
        assert str(reql1) == str(reql2)

    def test_skip(self):
        reql1 = self.reqlify(lambda: reqon.terms.skip(self.reql, 100))
        reql2 = self.reqlify(lambda: self.reql.skip(100))
        assert str(reql1) == str(reql2)

    def test_pluck(self):
        reql1 = self.reqlify(lambda: reqon.terms.pluck(self.reql, ['title', 'year']))
        reql2 = self.reqlify(lambda: self.reql.pluck('title', 'year'))
        assert str(reql1) == str(reql2)

    def test_sample(self):
        reql1 = self.reqlify(lambda: reqon.terms.sample(self.reql, 10))
        reql2 = self.reqlify(lambda: self.reql.sample(10))
        assert str(reql1) == str(reql2)

    def test_slice(self):
        reql1 = self.reqlify(lambda: reqon.terms.slice(self.reql, [10, 20]))
        reql2 = self.reqlify(lambda: self.reql.slice(10, 20))
        assert str(reql1) == str(reql2)




