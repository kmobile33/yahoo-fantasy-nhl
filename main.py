import datetime
import json
import time

from yahoo.fantasy_hockey_api import FantasyHockeyApi
from team import Team
from stats import Stats

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

def get_league_average_stats(teams):
    """Calculates an average of the average stats for each team"""
    list_of_team_averages = [x.average_stats for x in teams]

    return Stats.mean(list_of_team_averages)

def get_my_team_stat_deviation(api):
    teams = load_all_team_info(api)

    league_average_stats = get_league_average_stats(teams)

    my_team_avg_stats = [x for x in teams if x.is_my_team][0].average_stats

    return my_team_avg_stats.get_differentials(league_average_stats)

def main():
    api = FantasyHockeyApi('oauth.json', LEAGUE)
    deviation = get_my_team_stat_deviation(api)
    None

if __name__ == "__main__":
    main()
