import unittest

from reqon import utils

class UtilsTest(unittest.TestCase):
    def test_expand_path(self):
        expanded = utils.expand_path('foo.bar.baz')
        expected = {'foo': {'bar': {'baz': True}}}
        assert expected == expanded

    def test_expand_path_single(self):
        expanded = utils.expand_path('foo')
        expected = 'foo'
        assert expected == expanded

    def test_expand_path_non_string(self):
        expanded = utils.expand_path([1, 2, 3])
        expected = [1, 2, 3]
        assert expanded == expected

    def test_expand_paths(self):
        expanded = utils.expand_paths(['foo.bar.baz'])
        expected = [{'foo': {'bar': {'baz': True}}}]
        assert expected == expanded

    def test_expand_paths_single(self):
        expanded = utils.expand_paths(['foo'])
        expected = ['foo']
        assert expected == expanded
