class Team:
    def __init__(self, raw_team_info, roster_info = None, matchup_info = None):
        self.name = raw_team_info['name']
        self.id = raw_team_info['team_id']
        self.is_my_team = bool(raw_team_info['is_owned_by_current_login'])
        self.waiver_priority = raw_team_info['waiver_priority']
        self.move_count = raw_team_info['number_of_moves']
        self.trade_count = raw_team_info['number_of_trades']
