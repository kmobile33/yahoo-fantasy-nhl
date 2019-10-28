import unittest
import NHL

class TestNHL(unittest.TestCase):
    def test_get_player_id(self):
        nhl = NHL.NHL()
        player_id = nhl.get_player_id("Brad Marchand", "Boston Bruins")
        None