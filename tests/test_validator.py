import pytest
import reqon
import unittest

from .utils import ReQONTestMixin


class QueryValidatorTests(ReQONTestMixin, unittest.TestCase):
    def test_empty_query(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': []
        }
        reqon.validate_query(query)

    def test_no_db(self):
        query = {
            '$table': 'movies',
            '$query': []
        }
        reqon.validate_query(query)

    def test_missing_table(self):
        query = {
            '$db': 'test',
            '$query': []
        }
        with pytest.raises(reqon.exceptions.ValidationError):
            reqon.validate_query(query)

    def test_term_args(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': [
                ['$pluck', {'fields': ['name', 'year', 'rating']}]
            ]
        }
        reqon.validate_query(query)

    def test_term_noargs(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': [
                ['$count']
            ]
        }
        reqon.validate_query(query)

    def test_invalid_query(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': 'lol nope'
        }
        with pytest.raises(reqon.exceptions.ValidationError):
            reqon.validate_query(query)

    def test_invalid_term(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': [
                ['lol nope']
            ]
        }
        with pytest.raises(reqon.exceptions.ValidationError):
            reqon.validate_query(query)
