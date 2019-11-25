import datetime
import json
import time

from yahoo.fantasy_hockey_api import FantasyHockeyApi
from team import Team

GAME = 386
LEAGUE = 75370
TEAM = 5

def load_all_team_info(api):
    teams = [Team(x) for x in api.get_all_teams()]

    for team in teams:
        team.update_matchups(api.get_team_matchups(team.id))

def get_team_matchup_data(api, teams):
    return [Team(x) for x in api.get_team_matchups()]

def main():
    api = FantasyHockeyApi('oauth.json', LEAGUE)
    teams = load_all_team_info(api)
    None

if __name__ == "__main__":
    main()
