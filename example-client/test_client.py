import datetime
import reqon_client as rc
import unittest


class FilterFunctionTests(unittest.TestCase):
    def test_query(self):
        print rc.Query('player').filter(
            rc.row('games_won.championships') > 5,
            rc.row('birthday').date() >= datetime.date(1987, 7, 24)
        ).as_json()
