import geojson
import pytest
import reqon
import unittest

from reqon.validators import validate_query, validate_geojson

from .utils import ReQONTestMixin


class QueryValidatorTests(ReQONTestMixin, unittest.TestCase):
    def test_empty_query(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': []
        }
        validate_query(query)

    def test_no_db(self):
        query = {
            '$table': 'movies',
            '$query': []
        }
        validate_query(query)

    def test_missing_table(self):
        query = {
            '$db': 'test',
            '$query': []
        }
        with pytest.raises(reqon.exceptions.ValidationError):
            validate_query(query)

    def test_term_args(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': [
                ['$pluck', {'fields': ['name', 'year', 'rating']}]
            ]
        }
        validate_query(query)

    def test_term_noargs(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': [
                ['$count']
            ]
        }
        validate_query(query)

    def test_invalid_query(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': 'lol nope'
        }
        with pytest.raises(reqon.exceptions.ValidationError):
            validate_query(query)

    def test_invalid_term(self):
        query = {
            '$db': 'test',
            '$table': 'movies',
            '$query': [
                ['lol nope']
            ]
        }
        with pytest.raises(reqon.exceptions.ValidationError):
            validate_query(query)


class GeoJSONValidatorTests(ReQONTestMixin, unittest.TestCase):
    def test_valid_point(self):
        point = geojson.utils.generate_random('Point')
        validate_geojson(point)

    def test_invalid_point(self):
        point = {'type': 'Point', 'coordinates': 'lol nope'}
        with pytest.raises(reqon.exceptions.ValidationError):
            validate_geojson(point)

    def test_valid_linestring(self):
        linestring = geojson.utils.generate_random('LineString')
        validate_geojson(linestring)

    def test_invalid_linestring(self):
        linestring = {'type': 'LineString', 'coordinates': 'lol nope'}
        with pytest.raises(reqon.exceptions.ValidationError):
            validate_geojson(linestring)

    def test_valid_polygon(self):
        polygon = geojson.utils.generate_random('Polygon')
        validate_geojson(polygon)

    def test_invalid_polygon(self):
        polygon = {'type': 'Polygon', 'coordinates': 'lol nope'}
        with pytest.raises(reqon.exceptions.ValidationError):
            validate_geojson(polygon)

    def test_valid_circle(self):
        circle = geojson.utils.generate_random('Point')
        circle.update({
            'type': 'Circle',
            'radius': 10,
            'unit': 'km'
        })
        validate_geojson(circle)

    def test_invalid_circle(self):
        circle = {'type': 'Circle', 'coordinates': 'lol nope'}
        with pytest.raises(reqon.exceptions.ValidationError):
            validate_geojson(circle)
