from quart import Quart, jsonify

app = Quart(__name__)
app.bot = None


@app.route("/")
async def no():
    return jsonify({'no': 'go away'})


@app.route("/api/ping")
async def wsping():
    return jsonify({'ws': app.bot.latency})


@app.route("/api/stats")
async def stats():
    return jsonify({
        'ready': True,
        'guilds': len(app.bot.guilds),
        'shards': len(app.bot.shards)
    })
