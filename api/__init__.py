import flask
from yahoo.fantasy_hockey_api import XmlFantasyHockeyApi

app = flask.Flask(__name__)
app.config["DEBUG"] = True

yahoo_api = XmlFantasyHockeyApi('oauth.json', 52805)

import api.routes

app.run()