import json
from flask import jsonify, Response
from api import app, yahoo_api
from models.team import Team


@app.route('/', methods=['GET'])
def home():
    return("<p>This is the api!</p>")

@app.route('/team', methods=['GET'])
def teams():
    """Gets the team info from the Yahoo API and creates a list of Team objects"""
    teams = []
    for team_data in yahoo_api.get_all_teams():
        # Get matchup data from API
        matchup_data = yahoo_api.get_team_matchups(team_data['team_id'])

        # Create a Team object with team and matchup info
        teams.append(Team.from_api_data_with_matchups(team_data, matchup_data))

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
