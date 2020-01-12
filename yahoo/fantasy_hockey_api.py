import xml.etree.ElementTree as et
from yahoo.yahoo_api import YahooApi
from utilities import utilities

class FantasyHockeyApi(YahooApi):
    def __init__(self, credentials, league_id, game_id=None):
        super().__init__(credentials)
        self.base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
        self.game = game_id or self.get_game()
        self.league = league_id

    def get_team(self, team_id, format='json'):
        response = self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/", format=format)
        try:
            raw_team_data = self.__flatten_list_of_dicts(response['fantasy_content']['team'][0])
        except KeyError as err:
            if "fantasy_content" in err.args:
                # The request was successful, but there was no matching team ID
                return None
        return raw_team_data

    def get_team_matchups(self, team_id, format='json'):
        """For a given team, fetch matchup data for all weeks of the season, including stat results"""
        response = self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/matchups/", format='json')
        raw_matchup_data = response['fantasy_content']['team'][1]['matchups']

        matchups = []
        for key in raw_matchup_data.keys():
            if utilities.safe_cast(key, int):
                # Save matchup info dictionary
                matchup_info = raw_matchup_data[key]['matchup']

                # The stat info is nested, so the following is to un-nest it and put it directly in this dictionary
                matchup_team_dictionary = raw_matchup_data[key]['matchup']['0']['teams']
                for mk in matchup_team_dictionary.keys():
                    if utilities.safe_cast(mk, int) != None:
                        team_info = self.__flatten_list_of_dicts(matchup_team_dictionary[mk]['team'][0])
                        # Check if we have the target team_id, and if so, gather the stats
                        if (utilities.safe_cast(mk, int) != None) and (team_info['team_id'] == team_id):
                            # Set the 'stats' part of the matchup info and jump out
                            matchup_info['stats'] = matchup_team_dictionary[mk]['team'][1]['team_stats']['stats']
                            break

                if 'stats' not in matchup_info.keys():
                    raise Exception("Could not find stats info for " + str(team_id))

                # Remove un-needed info from dictionary before moving on
                matchup_info.pop("0")
                
                matchups.append(matchup_info)

        return matchups

    def get_all_teams(self, format='json'):
        """Gets a list of teams participating in the fantasy league along with their basic team info"""
        response = self.get(self.base_url + "/league/" + str(self.game) + ".l." + str(self.league) + "/teams/", format=format)
        raw_team_list = response['fantasy_content']['league'][1]['teams']
        
        # Flatten the team info, because Yahoo's JSON is very packed with garbage info
        team_list = []
        for key in raw_team_list.keys():
            # Remove non-team dict entries from processing
            if (utilities.safe_cast(key, int)):
                team_info = self.__flatten_list_of_dicts(raw_team_list[key]['team'][0])
                # Add team info dict to the overall list of teams
                team_list.append(team_info)
        
        return team_list

    def get_team_roster(self, team_id, format='json'):
        return self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/roster/", format=format)

    def get_game(self, format='json'):
        """Fetches the game ID for the current NHL season in Yahoo"""
        response = self.get(self.base_url + "game/nhl", format=format)
        return response['fantasy_content']['game'][0]['game_id']

    def get_league(self, format='json'):
        return self.get(self.base_url + "league/" + str(self.game) + ".l." + str(self.league) + "/", format=format)

    def get_all_players(self, format='json'):
        return self.get(self.base_url + "league/" + str(self.game) + ".l." + str(self.league) + "/players/", format=format)

    def __flatten_list_of_dicts(self, list_of_dictionaries):
        """Flatten the list of property dictionaries into one dictionary. This ignores non-dictionaries in the list"""
        result_dict = {}
        for single_dictionary in list_of_dictionaries:
            if type(single_dictionary) == dict:
                result_dict.update(single_dictionary)

        return result_dict        


class XmlFantasyHockeyApi(YahooApi):
    
    def __init__(self, credentials, league_id, game_id=None):
        super().__init__(credentials)
        self.base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
        self._ns = {"yahoo": "http://fantasysports.yahooapis.com/fantasy/v2/base.rng"}
        self.game = game_id or self.get_game()
        self.league = league_id

    def get_game(self):
        """Gets the game ID for the current NHL season in Yahoo"""
        # Send the request
        url = self.base_url + "game/nhl"
        response = self.get(url, format='xml')

        # Convert XML text into object and get game ID
        game_id = et.fromstring(response)\
            .find('yahoo:game', self._ns)\
            .find('yahoo:game_id', self._ns)\
            .text

        return int(game_id)

    def get_team(self, team_id):
        """Gets the team info given a team's Yahoo specific team ID"""
        # Send request
        url = self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/"
        response = self.get(url, format='xml')
        
        # Convert XML text into object and return the outer team tag
        return et.fromstring(response)\
            .find('yahoo:team', self._ns)
