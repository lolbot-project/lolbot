from quart import Quart, g

from . import endpoints

app = Quart(__name__)
app.bot = None


@app.before_request
def assign_globals():
    g.bot = app.bot


app.register_blueprint(endpoints.api, url_prefix="/api")
