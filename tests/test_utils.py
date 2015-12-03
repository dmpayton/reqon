import unittest

from reqon import utils

class UtilsTest(unittest.TestCase):
    def test_dict_in(self):
        assert utils.dict_in([1, 2, {"foo": "bar"}])
        assert not utils.dict_in([1, 2])
