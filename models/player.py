import re

class Player:
    def __init__(self, raw_player_data):
        self.first_name = self.last_name = self.positions = self.team_name = self.team_key = None
        
        for item in raw_player_data[0]:
            if type(item) is dict:
                if 'name' in item.keys():
                    self.first_name = item['name']['ascii_first']
                    self.last_name = item['name']['ascii_last']
                elif 'display_position' in item.keys():
                    self.positions = item['display_position']
                elif 'editorial_team_full_name' in item.keys():
                    self.team_name = item['editorial_team_full_name']
                elif 'editorial_team_key' in item.keys():
                    match_string = r'nhl.t.([\d]*)'
                    self.team_key = re.match(match_string, item['editorial_team_key']).groups()[0]
