import datetime
import json
import time

from player import Player
from team import Team
from yahoo import Yahoo

GAME = 386
LEAGUE = 75370
TEAM = 5

base_url = "https://fantasysports.yahooapis.com/fantasy/v2/"
game_url = "game/" + str(GAME) + "/"
league_url = "league/" + str(GAME) + ".l." + str(LEAGUE) + "/"
team_url = "team/" + str(GAME) + ".l." + str(LEAGUE) + ".t." + str(TEAM) + "/"
roster_url = team_url + "roster/"
player_url = league_url + "players"

def get_total_starts():
    players = []
    yahoo = Yahoo('oauth.json')

    # Get players
    raw_player_data = yahoo.get(base_url + roster_url)['fantasy_content']['team'][1]['roster']['0']['players']
    for p in raw_player_data:
        if p != 'count':
            players.append(Player(raw_player_data[p]['player']))

    # Get teams and schedules
    teams = []
    team_keys = set([ x.team_key for x in players])
    for tk in team_keys:
        raw_team_data = yahoo.get(base_url + 'team/' + str(GAME) + '.l.' + str(LEAGUE) + '.t.' + str(tk))['fantasy_content']
        None


def main():
    get_total_starts()

if __name__ == "__main__":
    main()