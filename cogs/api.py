"""
API endpoints for lolbot.
If you're looking for the cog that powers the API,
you are in the wrong place. You are looking for
api_launcher.py.
"""

from quart import Quart, jsonify
from quart_cors import cors

app = Quart(__name__)
app = cors(app)
app.bot = None

# Basic shit
@app.route('/')
async def no():
    return jsonify({'no': 'go away'})


@app.route('/api/ping')
async def wsping():
    return jsonify({'ws': round(app.bot.latency, 3)})

@app.route('/api/votes')
async def votes():
    _id = app.bot.user.id
    dbl = await app.bot.session.get(f'https://discordbots.org/api/bots/{_id}')
    listcord = await app.bot.session.get(f'https://listcord.com/api/bot/{_id}')
    if dbl.status == 200:
        _dbl = await dbl.json()
        dbl_status = 200
        dbl_monthly = _dbl['monthlyPoints']
        dbl_total = _dbl['points']
    else:
        dbl_monthly = '0 (error)'
        dbl_total = '0 (error)'
        dbl_status = dbl.status
    if listcord.status == 200:
        _lc = await listcord.json()
        lc_status = 200
        lc_votes = _lc['votes']
    else:
        lc_status = listcord.status
        lc_votes = '0 (error)'

    return jsonify({
        'dbl_status': dbl_status,
        'dbl_monthly': dbl_monthly,
        'dbl_total': dbl_total,
        'lc_status': lc_status,
        'lc_votes': lc_votes
    })
# Stats endpoints
@app.route('/api/stats/<whatever>')
async def stats(whatever):
    if whatever == 'guilds':
        return jsonify({'guilds': len(app.bot.guilds)})
    elif whatever == 'shards':
        return jsonify({'shards': len(app.bot.shards)})
    elif whatever == 'ready':
        return jsonify({'ready': app.bot.is_ready()})
    elif whatever == 'all' or None:
        return jsonify({
            'ready': app.bot.is_ready(),
            'guilds': len(app.bot.guilds),
            'shards': len(app.bot.shards)
        })
    else:
        return jsonify({'error': 404})
