from yahoo.yahoo_api import YahooApi

class FantasyHockeyApi(YahooApi):
    def __init__(self, credentials, league_id, game_id=None):
        super().__init__(credentials)
        self.base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
        self.game = game_id or self.get_game()
        self.league = league_id

    def get_team(self, team_id):
        response = self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/")
        return response['fantasy_content']['team']

    def get_team_matchups(self, team_id):
        response = self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/matchups/")
        raw_matchup_data = response['fantasy_content']['team'][1]['matchups']

        matchups = []
        for key in raw_matchup_data.keys():
            if self.__safe_cast(key, int):
                # Save matchup info dictionary
                matchup_info = raw_matchup_data[key]['matchup']

                # The stat info is nested, so the following is to un-nest it and put it directly in this dictionary
                matchup_team_dictionary = raw_matchup_data[key]['matchup']['0']['teams']
                for mk in matchup_team_dictionary.keys():
                    if self.__safe_cast(mk, int) != None:
                        team_info = self.__flatten_list_of_dicts(matchup_team_dictionary[mk]['team'][0])
                        # Check if we have the target team_id, and if so, gather the stats
                        if (self.__safe_cast(mk, int) != None) and (team_info['team_id'] == team_id):
                            # Set the 'stats' part of the matchup info and jump out
                            matchup_info['stats'] = matchup_team_dictionary[mk]['team'][1]['team_stats']['stats']
                            break

                if 'stats' not in matchup_info.keys():
                    raise Exception("Could not find stats info for " + str(team_id))

                # Remove un-needed info from dictionary before moving on
                matchup_info.pop("0")
                
                matchups.append(matchup_info)

        return matchups

    def get_all_teams(self):
        response = self.get(self.base_url + "/league/" + str(self.game) + ".l." + str(self.league) + "/teams/")
        raw_team_list = response['fantasy_content']['league'][1]['teams']
        
        # Flatten the team info, because Yahoo's JSON is very packed with garbage info
        team_list = []
        for key in raw_team_list.keys():
            # Remove non-team dict entries from processing
            if (self.__safe_cast(key, int)):
                team_info = self.__flatten_list_of_dicts(raw_team_list[key]['team'][0])
                # Add team info dict to the overall list of teams
                team_list.append(team_info)
        
        return team_list

    def get_team_roster(self, team_id):
        return self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/roster/")

    def get_game(self):
        """Fetches the game ID for the current NHL season in Yahoo"""
        response = self.get(self.base_url + "game/nhl")
        return response['fantasy_content']['game'][0]['game_id']

    def get_league(self):
        return self.get(self.base_url + "league/" + str(self.game) + ".l." + str(self.league) + "/")

    def get_all_players(self):
        return self.get(self.base_url + "league/" + str(self.game) + ".l." + str(self.league) + "/players/")

    def __safe_cast(self, val, to_type, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default

    def __flatten_list_of_dicts(self, list_of_dictionaries):
        """Flatten the list of property dictionaries into one dictionary.This ignores non-dictionaries in the list"""
        result_dict = {}
        for single_dictionary in list_of_dictionaries:
            if type(single_dictionary) == dict:
                result_dict.update(single_dictionary)

        return result_dict        
        