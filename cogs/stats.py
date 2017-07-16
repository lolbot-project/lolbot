import json
import logging
import aiohttp

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
config = json.load(open('config.json'))

class Stats:
  async def listpost(self, bot):
    payload = json.dumps({
      'server_count': len(bot.guilds)
    })
    session = aiohttp.ClientSession()
    if config['dbotsorg'] == False:
      logging.info('not posting to discordbots.org')
    else:
      dbl_headers = {
        'Authorization': config['dbl'],
        'Content-Type': 'application/json'
      }
      dbl_url = 'https://discordbots.org/api/bots/' + config['botid'] + '/stats'
      async with session.post(dbl_url, data=self.payload, headers=dbl_headers) as dbl_resp:
        if dbl_resp.status == 200:
          logging.info('dbl: posted!')
        else:
          logging.info(f'dbl: something weird happened: code {dbl_resp.status}.')                                                   

    if config['dbotspw'] == False:
      logging.info('not posting to bots.discord.pw')
    else:
      headers = {
        'Authorization': config['dbots'],
        'Content-Type': 'application/json'
      }
      dbots_url = 'https://bots.discord.pw/api/bots/' + config['botid'] + '/stats'
      async with session.post(dbots_url, data=payload, headers=headers) as resp:
        assert resp.status == 200
        logging.info('dbots: posted!')

  def __init__(self, bot):
    self.bot = bot
    self.post = listpost

  async def on_guild_join( self, guild ):
    logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
    await listpost()

  async def on_guild_remove( self, guild ):
    logging.info('Left ' + str(guild.name))
    await listpost()

def setup(bot):
  bot.add_cog(Stats(bot))
