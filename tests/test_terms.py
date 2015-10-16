import reqon
import rethinkdb as r
import unittest


class TermsTests(unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_group(self):
        reql1 = reqon.terms.group(self.reql, 'rating')
        reql2 = self.reql.group('rating')
        print()
        print(reql1)
        print(reql2)
