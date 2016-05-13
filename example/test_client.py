import datetime
import unittest

from .client import Query, Field


class FilterFunctionTests(unittest.TestCase):
    def test_query(self):
        print(Query('player').filter(
            Field('games_won.championships') > 5,
            Field('birthday').date() >= datetime.date(1987, 7, 24)
        ).as_json())
