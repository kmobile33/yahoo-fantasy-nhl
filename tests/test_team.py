import unittest
import xml.etree.ElementTree as et

from models.team import Team

class TestTeamMethods(unittest.TestCase):
    def test_xml_constructor(self):
        ns = {"ns": "http://fantasysports.yahooapis.com/fantasy/v2/base.rng"}
        xml = et.parse('./sample-api-responses/get_team.xml').find('ns:team', ns)
        
        result = Team.from_xml_api_data(xml)

        expected = Team(**{
            "name": "K.E.V.I.N",
            "id": 5,
            "owner": "Kevin",
            "is_my_team": True,
            "waiver_priority": 5,
            "move_count": 26,
            "trade_count": 0,
            "matchups": [],
            "average_stats": None,
        })

        self.assertEqual(expected.name, result.name)
        self.assertEqual(expected.id, result.id)
        self.assertEqual(expected.owner, result.owner)
        self.assertEqual(expected.is_my_team, result.is_my_team)
        self.assertEqual(expected.waiver_priority, result.waiver_priority)
        self.assertEqual(expected.move_count, result.move_count)
        self.assertEqual(expected.trade_count, result.trade_count)
        self.assertEqual(expected.matchups, result.matchups)
        self.assertEqual(expected.average_stats, result.average_stats)

