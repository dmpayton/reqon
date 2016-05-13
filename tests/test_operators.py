import reqon
import rethinkdb as r
import unittest

from reqon import operators
from .utils import ReQONTestMixin

class OperatorsTests(ReQONTestMixin, unittest.TestCase):
    def setUp(self):
        self.reql = r.table('movies')

    def test_build(self):
        response = operators.build(['$in', [1, 2, 3]])
        assert str(response) == "(r.row['$in'] == r.expr([1, 2, 3]))"

    def test_build_attribute(self):
        response = operators.build_attribute("$in", [1, 2, 3])
        assert str(response) == "(r.row['$in'] == r.expr([1, 2, 3]))"

    def test_in_(self):
        response = operators.in_(r.row["score"], [1, 2, 3])(r.row)
        assert str(response) == "r.expr([1, 2, 3]).contains(lambda var_1: r.row['score'])"

    def test_regex(self):
        response = operators.regex(r.row["name"], "^foo")
        assert str(response) == "r.row['name'].coerce_to('string').match('^foo')"

    def test_ieq(self):
        response = operators.ieq(r.row["name"], "foo")
        assert str(response) == "r.row['name'].coerce_to('string').match('(?i)^foo$')"

    def test_starts(self):
        response = operators.starts(r.row["name"], "d")
        assert str(response) == "r.row['name'].coerce_to('string').match('^d')"

    def test_istarts(self):
        response = operators.istarts(r.row["name"], "d")
        assert str(response) == "r.row['name'].coerce_to('string').match('(?i)^d')"

    def test_ends(self):
        response = operators.ends(r.row["name"], "n")
        assert str(response) == "r.row['name'].coerce_to('string').match('n$')"

    def test_iends(self):
        response = operators.iends(r.row["name"], "n")
        assert str(response) == "r.row['name'].coerce_to('string').match('(?i)n$')"

    def test_includes(self):
        point = {
            "type": "Point",
            "coordinates": [-135.4, -38.4]
        }
        response = operators.includes(r.row["area"], point)
        assert str(response) == "r.row['area'].includes(r.point(-135.4, -38.4))"

    def test_intersects(self):
        polygon = {
            "type": "Polygon",
            "coordinates": [[[-116, 28], [13, -26], [59, 58], [-116, 28]]]
        }
        response = operators.intersects(r.row["area"], polygon)
        assert str(response) == "r.row['area'].intersects(r.polygon([-116, 28], [13, -26], [59, 58], [-116, 28]))"
