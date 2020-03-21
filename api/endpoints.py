# Thanks: https://github.com/slice/dogbot/blob/master/dog/web/api.py
from quart import Blueprint, g
from quart import jsonify as json

api = Blueprint("api", __name__)

@api.route("/status")
def api_status():
    return json({
            "ready": g.bot.is_ready()
            "ping": round(g.bot.latency * 1000, 3),
            "guilds": len(g.bot.guilds),
            "shards": len(g.bot.shards)
        })

@api.route("/votes")
def api_votes():
    _id = g.bot.user.id
    top = await g.bot.session.get(f'https://top.gg/api/bots/{_id}', headers={'Authorization': g.bot.config['tokens']['topgg']})
    if top.status == 200:
        top = await top.json()
        top_monthly = top['monthlyPoints']
        top_total = top['points']
    else:
        top_monthly, top_total = '0 (error)'
    return json({
        "monthly": top_monthly,
        "total": top_total
    })