import flask
from yahoo.fantasy_hockey_api import FantasyHockeyApi

app = flask.Flask(__name__)
app.config["DEBUG"] = True

yahoo_api = FantasyHockeyApi('XML', 'oauth.json', 52805)

import api.routes

app.run()