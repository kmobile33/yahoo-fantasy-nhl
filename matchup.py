from datetime import datetime

from stats import Stats

class Matchup():
    def __init__(self, raw_matchup_info, team_id):
        now = datetime.now()
        self.week = raw_matchup_info['week']
        self.week_start = datetime.strptime(raw_matchup_info['week_start'], "%Y-%m-%d")
        self.week_end = datetime.strptime(raw_matchup_info['week_end'], "%Y-%m-%d")
        self.started = (self.week_start < now)
        self.complete = (self.week_end < now)
        self.is_tied = None if not self.complete else bool(raw_matchup_info['is_tied'])
        self.won = None if (not self.complete or self.is_tied)\
            else bool(raw_matchup_info['winner_team_key'][(raw_matchup_info['winner_team_key'].rfind(".") + 1):] == team_id)
        self.stats = None if not self.started else Stats(raw_matchup_info['stats'])
