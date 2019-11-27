from datetime import datetime

from matchup import Matchup

class Team:
    def __init__(self, raw_team_info, roster_info = None, matchup_info = None):
        self.name = raw_team_info['name']
        self.id = raw_team_info['team_id']
        self.owner = raw_team_info['managers'][0]['manager']['nickname']
        self.is_my_team = 'is_owned_by_current_login' in raw_team_info.keys()
        self.waiver_priority = raw_team_info['waiver_priority']
        self.move_count = raw_team_info['number_of_moves']
        self.trade_count = raw_team_info['number_of_trades']

        self.machups = []

    def update_matchups(self, raw_matchup_info):
        for raw_matchup in raw_matchup_info:
            if ( datetime.strptime(raw_matchup['week_start'], "%Y-%m-%d") < datetime.now()):
                self.machups.append(Matchup(raw_matchup, self.id))

