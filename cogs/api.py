"""
API endpoints for lolbot.
If you're looking for the cog that powers the API,
you are in the wrong place. You are looking for
api_launcher.py.
"""
from quart import Quart, jsonify

app = Quart(__name__)
app.bot = None

app.cors = {
    'Access-Control-Allow-Origin': '*'
}


# Basic shit
@app.route("/")
async def no():
    return jsonify({'no': 'go away'}), app.cors


@app.route("/api/ping")
async def wsping():
    return jsonify({'ws': round(app.bot.latency, 3)}), app.cors


# Stats endpoints
@app.route("/api/stats/<whatever>")
async def stats(whatever):
    if whatever == 'guilds':
        return jsonify({'guilds': len(app.bot.guilds)}), app.cors
    elif whatever == 'shards':
        return jsonify({'shards': len(app.bot.shards)}), app.cors
    elif whatever == 'ready':
        return jsonify({'ready': app.bot.is_ready()}), app.cors
    elif whatever == 'all' or None:
        return jsonify({
            'ready': app.bot.is_ready(),
            'guilds': len(app.bot.guilds),
            'shards': len(app.bot.shards)
        }), app.cors
    else:
        return jsonify({'error': 404})
