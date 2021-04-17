from quart import Blueprint, g
from quart import jsonify as json
from quart.utils import redirect
from urllib.parse import urlencode
from itsdangerous import Signer
import rstr
from random import SystemRandom

api = Blueprint(__name__)
state_signer = Signer(g.config['api']['secret_key'])
state_string = rstr.Rstr(SystemRandom())

@api.route('/authorize')
async def authorize():
    strings = urlencode({
        'client_id': g.config['tokens']['osu_client_id'],
        'redirect_uri': f'{g.config["api"]["root"]}/api/osu/finish_auth',
        'response_type': 'code',
        'scope': 'public',
        'state': state_signer.sign(state_string.urlsafe())
    })
    return redirect(f'https://osu.ppy.sh/oauth/authorize?{strings}')

@api.route('/finish_auth')
async def finish_authorization():
    # TBD: figure out how to carry the key across
    return NotImplemented
