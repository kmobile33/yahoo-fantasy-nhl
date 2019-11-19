from yahoo.yahoo_api import YahooApi

class FantasyHockeyApi(YahooApi):
    def __init__(self, credentials, league_id):
        self.base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
        self.game = 386
        self.league = league_id

        super().__init__(credentials)

    def get_team(self, team_id):
        response = self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/")
        return response['fantasy_info']['team']

    def get_team_matchups(self, team_id):
        response = self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/matchups/")
        return response['fantasy_info']['team']

    def get_all_teams(self):
        response = self.get(self.base_url + "team/")
        return response['fantasy_info']['team']

    def get_team_roster(self, team_id):
        return self.get(self.base_url + "team/" + str(self.game) + ".l." + str(self.league) + ".t." + str(team_id) + "/roster/")

    def get_game(self):
        return self.get(self.base_url + "game/" + str(self.game) + "/")

    def get_league(self):
        return self.get(self.base_url + "league/" + str(self.game) + ".l." + str(self.league) + "/")

    def get_all_players(self):
        return self.get(self.base_url + "league/" + str(self.game) + ".l." + str(self.league) + "/players/")
