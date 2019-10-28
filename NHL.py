import json
import urllib.request

class NHL:
    base_api = "https://statsapi.web.nhl.com/api/v1/"

    def get_player_id(self, player_name, team_name):
        teams = ""
        with urllib.request.urlopen(self.base_api + "teams") as response:
            teams_response = json.loads(response.read())
            teams = teams_response["teams"]

        selected_team = (x for x in teams if x["name"] == team_name)

        # with urllib.request.urlopen(self.base_api + "team") as response:
        #     html = response.read()

        return teams_response 

    def get_player_game_log(self, player_id):
        #https://statsapi.web.nhl.com/api/v1/people/8471233/stats?stats=gameLog&season=20192020
        raise NotImplementedError

    def get_player_cummulative_stats(self, player_id):
        # https://statsapi.web.nhl.com/api/v1/people/8471233/stats?stats=statsSingleSeason&season=20182019
        raise NotImplementedError

    def get_team_schedule(self, team_name):
        raise NotImplementedError
