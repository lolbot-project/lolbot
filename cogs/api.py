"""
API endpoints for lolbot.
If you're looking for the cog that powers the API,
you are in the wrong place. You are looking for
api_launcher.py.
"""
from quart import Quart, jsonify

app = Quart(__name__)
app.bot = None

# Basic shit
@app.route("/")
async def no():
    return jsonify({'no': 'go away'})


@app.route("/api/ping")
async def wsping():
    return jsonify({'ws': round(app.bot.latency, 3)})


# Stats endpoints
@app.route("/api/stats/<whatever>")
async def stats(whatever):
    if whatever is 'guilds':
        return jsonify({'guilds': len(app.bot.guilds)})
    elif whatever is 'shards':
        return jsonify({'shards': len(app.bot.shards)})
    elif whatever is 'ready':
        return jsonify({'ready': app.bot.is_ready()})
    elif whatever is 'all':
        return jsonify({
            'ready': app.bot.is_ready(),
            'guilds': len(app.bot.guilds),
            'shards': len(app.bot.shards)
        })
    else:
        return jsonify({'error': 404})
