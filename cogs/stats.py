import json
import logging
import aiohttp

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
config = json.load(open('config.json'))

class Stats:
  def __init__(self, bot):
    self.bot = bot
    self.session = aiohttp.ClientSession(loop=self.bot.loop)
    self.payload = json.dumps({
      'server_count': len(self.bot.guilds)
    })

 
  async def listpost(self):
    if config['dbotsorg'] == False:
      logging.info('not posting to discordbots.org')
    else:
      dbl_headers = {
        'Authorization': config['dbl'],
        'Content-Type': 'application/json'
      }
      dbl_url = 'https://discordbots.org/api/bots/' + config['botid'] + '/stats'
      async with self.session.post(dbl_url, data=self.payload, headers=dbl_headers) as dbl_resp:
        assert dbl_resp.status == 200
        logging.info('dbl: posted!')

    if config['dbotspw'] == False:
      logging.info('not posting to bots.discord.pw')
    else:
      headers = {
        'Authorization': config['dbots'],
        'Content-Type': 'application/json'
      }
      dbots_url = 'https://bots.discord.pw/api/bots/' + config['botid'] + '/stats'
      async with self.session.post(dbots_url, data=self.payload, headers=headers) as resp:
        assert resp.status == 200
        logging.info('dbots: posted!')

  async def on_guild_join( self, guild ):
    logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
    await listpost()

  async def on_guild_remove( self, guild ):
    logging.info('Left ' + str(guild.name))
    await listpost()

def setup(bot):
  bot.add_cog(Stats(bot))
