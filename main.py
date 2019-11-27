import datetime
import json
import time

from yahoo.fantasy_hockey_api import FantasyHockeyApi
from team import Team

LEAGUE = 52805 #75370
TEAM = 5

def load_all_team_info(api):
    """Gets the team info from the Yahoo API and creates a list of Team objects"""
    teams = []
    for team_data in api.get_all_teams():
        # Get matchup data from API
        matchup_data = api.get_team_matchups(team_data['team_id'])

        # Create a Team object with team and matchup info
        teams.append(Team.from_api_data_with_matchups(team_data, matchup_data))

    return teams

def main():
    api = FantasyHockeyApi('oauth.json', LEAGUE)
    teams = load_all_team_info(api)
    None

if __name__ == "__main__":
    main()
