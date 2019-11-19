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

def main():
    api = FantasyHockeyApi('oauth.json', LEAGUE)
    test = api.get_team_matchups(1)
    #load_all_team_info(api)
    # get_total_starts(api)
    None

if __name__ == "__main__":
    main()
