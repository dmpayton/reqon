import reqon
import rethinkdb as r
import unittest

from .utils import ReQONTestMixin


class TermsTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_group(self):
        reql1 = reqon.terms.group(self.reql, 'rating')
        reql2 = self.reql.group('rating')
