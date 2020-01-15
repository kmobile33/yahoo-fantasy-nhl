import unittest
from datetime import datetime
import xml.etree.ElementTree as et

from models.matchup import Matchup

class TestMatchupMethods(unittest.TestCase):
    def test_xml_constructor(self):
        ns = {"ns": "http://fantasysports.yahooapis.com/fantasy/v2/base.rng"}
        xml = et.parse('./sample-api-responses/matchup.xml').find('ns:matchup', ns)

        result = Matchup.from_xml_api_data(xml, 5)

        expected = Matchup(**{
            'week': 1,
            'week_start': datetime.strptime('2019-10-02', "%Y-%m-%d"),
            'week_end': datetime.strptime('2019-10-13', "%Y-%m-%d"),
            'has_started': True,
            'is_complete': True,
            'is_tied': False,
            'won': False,
            'stats': []
        })

        # Stats are omitted since they will be tested via the Stat class unit tests
        self.assertEqual(expected.week, result.week)
        self.assertEqual(expected.week_start, result.week_start)
        self.assertEqual(expected.week_end, result.week_end)
        self.assertEqual(expected.has_started, result.has_started)
        self.assertEqual(expected.is_complete, result.is_complete)
        self.assertEqual(expected.is_tied, result.is_tied)
        self.assertEqual(expected.won, result.won)
        self.assertEqual(expected.stats, result.stats)
        