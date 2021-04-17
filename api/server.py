from quart import Quart, g

import bp

app = Quart(__name__)
app.bot = None


@app.before_request
def assign_globals():
    g.bot = app.bot
    g.config = app.bot.config


app.register_blueprint(bp.basic.api, url_prefix="/api/basic")
app.register_blueprint(bp.osuauth.api, url_prefix="/api/osu")
