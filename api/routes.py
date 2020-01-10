import json
from flask import jsonify, Response
from api import app, yahoo_api
from models.team import Team
from models.stats import Stats


@app.route('/', methods=['GET'])
def home():
    return("<p>This is the api!</p>")

@app.route('/team', methods=['GET'])
def teams():
    """Gets the team info from the Yahoo API and creates a list of Team objects"""
    teams = _get_all_team_info()
    raw_json = json.dumps(teams, default=Team.serialize) #[json.dumps(x, default=Team.serialize) for x in teams]

    return Response(
        response=raw_json,
        status=200,
        mimetype='application/json'
    )

@app.route('/team/<int:id>')
def team(id):
    raw_team_data = yahoo_api.get_team(id)

    if not raw_team_data:
        return Response(response="Team does not exist", status=400)

    team = Team.from_raw_api_data(yahoo_api.get_team(id))

    return Response(
        response=json.dumps(team, default=Team.serialize),
        status=200,
        mimetype='application/json'
    )

@app.route('/team/<int:team_1_id>/compare_stats/<int:team_2_id>')
def compare_team_averages(team_1_id, team_2_id):
    teams = _get_all_team_info()
    
    team_1_stats = [x for x in teams if x.id == str(team_1_id)][0].average_stats
    team_2_stats = [x for x in teams if x.id == str(team_2_id)][0].average_stats

    deviation = team_1_stats.get_differentials(team_2_stats)

    return Response(
        response=json.dumps(deviation, default=Stats.serialize),
        status=200,
        mimetype='application/json'
    )

@app.route('/compare_stat_averages/<int:id>')
def compare_stat_averages(id):
    teams = _get_all_team_info()

    league_average_stats = _get_league_average_stats(teams)

    selected_team_avg_stats = [x for x in teams if x.id == str(id)][0].average_stats

    deviation = selected_team_avg_stats.get_differentials(league_average_stats)
    
    return Response(
        response=json.dumps(deviation, default=Stats.serialize),
        status=200,
        mimetype='application/json'
    )

def _get_all_team_info():
    teams = []
    for team_data in yahoo_api.get_all_teams():
        # Get matchup data from API
        matchup_data = yahoo_api.get_team_matchups(team_data['team_id'])

        # Create a Team object with team and matchup info
        teams.append(Team.from_api_data_with_matchups(team_data, matchup_data))
    return teams

def _get_league_average_stats(teams):
    """Calculates an average of the average stats for each team"""
    list_of_team_averages = [x.average_stats for x in teams]

    return Stats.mean(list_of_team_averages)