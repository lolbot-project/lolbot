from quart import Quart, g

from .api import api

app = Quart(__name__)
app.bot = None

@app.before_request
def assign_globals():
    g.bot = app.bot

app.register_blueprint(api, url_prefix="/api")