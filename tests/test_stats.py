import unittest
import xml.etree.ElementTree as et

from models.stats import Stats

class TestStatMethods(unittest.TestCase):
    def setUp(self):
        self.stat_kwargs = {
            'goals' : 1,
            'assists' : 1,
            'penalty_minutes' : 1,
            'shots_on_goal' : 1,
            'hits' : 1,
            'blocks' : 1,
            'wins' : 1,
            'goalie_ga' : 1,
            'goalie_gaa' : 1.11,
            'goalie_sa' : 1,
            'goalie_so' : 1
        }

    def test_equality(self):
        stats_1 = Stats(**self.stat_kwargs)
        stats_2 = Stats(**self.stat_kwargs)

        self.assertTrue(stats_1 == stats_2)
        self.assertFalse(stats_1 != stats_2)

    def test_inequality(self):
        stats_1 = Stats(**self.stat_kwargs)
        
        self.stat_kwargs.update( {'goalie_gaa' : 1.12})
        stats_2 = Stats(**self.stat_kwargs)
        
        self.assertTrue( stats_1 != stats_2 )
        self.assertFalse( stats_1 == stats_2 )

    def test_less_than(self):
        stats_1 = Stats(**self.stat_kwargs)
        
        self.stat_kwargs.update( {'goalie_gaa' : 1.12})
        stats_2 = Stats(**self.stat_kwargs)

        self.assertTrue( stats_1 < stats_2 )
        self.assertFalse( stats_2 < stats_1 )

    def test_less_than_equal(self):
        stats_1 = Stats(**self.stat_kwargs)
        stats_2 = Stats(**self.stat_kwargs)
        
        self.assertTrue( stats_1 <= stats_2 )
        self.assertTrue( stats_2 <= stats_1)

    def test_greater_than(self):
        stats_1 = Stats(**self.stat_kwargs)
        
        self.stat_kwargs.update( {'goalie_gaa' : 1.12})
        stats_2 = Stats(**self.stat_kwargs)

        self.assertTrue( stats_2 > stats_1 )
        self.assertFalse( stats_1 > stats_2 )

    def test_greater_than_equal(self):
        stats_1 = Stats(**self.stat_kwargs)
        stats_2 = Stats(**self.stat_kwargs)
        
        self.assertTrue( stats_1 >= stats_2 )
        self.assertTrue( stats_2 >= stats_1)

    def test_add(self):
        stats_1 = Stats(**self.stat_kwargs)
        stats_2 = Stats(**self.stat_kwargs)

        result = stats_1 + stats_2

        self.assertEqual(result.goals, 2)
        self.assertEqual(result.assists, 2)
        self.assertEqual(result.penalty_minutes, 2)
        self.assertEqual(result.shots_on_goal, 2)
        self.assertEqual(result.hits, 2)
        self.assertEqual(result.blocks, 2)
        self.assertEqual(result.wins, 2)
        self.assertEqual(result.goalie_ga, 2)
        self.assertEqual(result.goalie_gaa, 2.22)
        self.assertEqual(result.goalie_sa, 2)
        self.assertEqual(result.goalie_so, 2)

    def test_div(self):
        stats_1 = Stats(**self.stat_kwargs)

        result = stats_1 / 2

        self.assertEqual(result.goals, 0.5)
        self.assertEqual(result.assists, 0.5)
        self.assertEqual(result.penalty_minutes, 0.5)
        self.assertEqual(result.shots_on_goal, 0.5)
        self.assertEqual(result.hits, 0.5)
        self.assertEqual(result.blocks, 0.5)
        self.assertEqual(result.wins, 0.5)
        self.assertEqual(result.goalie_ga, 0.5)
        self.assertEqual(result.goalie_gaa, 0.555)
        self.assertEqual(result.goalie_sa, 0.5)
        self.assertEqual(result.goalie_so, 0.5)

    def test_mean(self):
        stat_kwargs_1 = {
            'goals' : 2,
            'assists' : 2,
            'penalty_minutes' : 2,
            'shots_on_goal' : 2,
            'hits' : 2,
            'blocks' : 2,
            'wins' : 2,
            'goalie_ga' : 2,
            'goalie_gaa' : 2.00,
            'goalie_sa' : 2,
            'goalie_so' : 2
        }

        stat_kwargs_2 = {
            'goals' : 4,
            'assists' : 4,
            'penalty_minutes' : 4,
            'shots_on_goal' : 4,
            'hits' : 4,
            'blocks' : 4,
            'wins' : 4,
            'goalie_ga' : 4,
            'goalie_gaa' : 4.00,
            'goalie_sa' : 4,
            'goalie_so' : 4
        }

        stats_1 = Stats(**stat_kwargs_1)
        stats_2 = Stats(**stat_kwargs_2)

        result = Stats.mean([stats_1, stats_2])
        self.assertEqual(result.goals, 3)
        self.assertEqual(result.assists, 3)
        self.assertEqual(result.penalty_minutes, 3)
        self.assertEqual(result.shots_on_goal, 3)
        self.assertEqual(result.hits, 3)
        self.assertEqual(result.blocks, 3)
        self.assertEqual(result.wins, 3)
        self.assertEqual(result.goalie_ga, 3)
        self.assertEqual(result.goalie_gaa, 3.00)
        self.assertEqual(result.goalie_sa, 3)
        self.assertEqual(result.goalie_so, 3)

    def test_from_api_data(self):
        stats_dict = {"stats": [
            {
                "stat": {
                    "stat_id": "1",
                    "value": "8"
                }
            },
            {
                "stat": {
                    "stat_id": "2",
                    "value": "16"
                }
            },
            {
                "stat": {
                    "stat_id": "5",
                    "value": "20"
                }
            },
            {
                "stat": {
                    "stat_id": "14",
                    "value": "97"
                }
            },
            {
                "stat": {
                    "stat_id": "31",
                    "value": "27"
                }
            },
            {
                "stat": {
                    "stat_id": "32",
                    "value": "33"
                }
            },
            {
                "stat": {
                    "stat_id": "19",
                    "value": "2"
                }
            },
            {
                "stat": {
                    "stat_id": "22",
                    "value": "2"
                }
            },
            {
                "stat": {
                    "stat_id": "23",
                    "value": "1.00"
                }
            },
            {
                "stat": {
                    "stat_id": "24",
                    "value": "45"
                }
            },
            {
                "stat": {
                    "stat_id": "27",
                    "value": "0"
                }
            }
        ]}

        result = Stats.from_api_data(stats_dict['stats'])
        self.assertEqual(result.goals, 8)
        self.assertEqual(result.assists, 16)
        self.assertEqual(result.penalty_minutes, 20)
        self.assertEqual(result.shots_on_goal, 97)
        self.assertEqual(result.hits, 27)
        self.assertEqual(result.blocks, 33)
        self.assertEqual(result.wins, 2)
        self.assertEqual(result.goalie_ga, 2)
        self.assertEqual(result.goalie_gaa, 1.00)
        self.assertEqual(result.goalie_sa, 45)
        self.assertEqual(result.goalie_so, 0)

    def test_from_xml_api_data(self):
        ns = {"ns": "http://fantasysports.yahooapis.com/fantasy/v2/base.rng"}
        stats_xml = et.parse('./sample-api-responses/stats.xml')\
            .find('ns:stats', ns)

        result = Stats.from_xml_api_data(stats_xml)

        expected = Stats(**{
            'goals': 16,
            'assists': 42,
            'penalty_minutes': 37,
            'shots_on_goal': 195,
            'hits': 89,
            'blocks': 63,
            'wins': 3,
            'goalie_ga': 24,
            'goalie_gaa': 2.94,
            'goalie_sa': 253,
            'goalie_so': 0
        })

        self.assertEqual(expected.goals, result.goals)
        self.assertEqual(expected.assists, result.assists)
        self.assertEqual(expected.penalty_minutes, result.penalty_minutes)
        self.assertEqual(expected.shots_on_goal, result.shots_on_goal)
        self.assertEqual(expected.hits, result.hits)
        self.assertEqual(expected.blocks, result.blocks)
        self.assertEqual(expected.wins, result.wins)
        self.assertEqual(expected.goalie_ga, result.goalie_ga)
        self.assertEqual(expected.goalie_gaa, result.goalie_gaa)
        self.assertEqual(expected.goalie_sa, result.goalie_sa)
        self.assertEqual(expected.goalie_so, result.goalie_so)
