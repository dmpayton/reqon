import reqon
import unittest
import pytest

class TestQuery(unittest.TestCase):
    def test_query(self):
        query = {
            "$table": "foo",
            "$query": [
                ["$get", "foo"]
            ]
        }

        assert str(reqon.query(query)) == "r.table('foo').get('foo')"

    def test_invalid_query(self):
        with pytest.raises(reqon.exceptions.ReqonError):
            reqon.query({"$schema": "foo"})
