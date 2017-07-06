import json
import logging
import aiohttp

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
config = json.load(open('config.json'))

class Stats:
  async def dbotsorg(self):
    payload = json.dumps({
      'server_count': len(self.bot.guilds)
    })
    dbl_headers = {
      'Authorization': config['dbl'],
      'Content-Type': 'application/json'
    }
    dbl_url = 'https://discordbots.org/api/bots/' + config['botid'] + '/stats'
    async with self.session.post(dbl_url, data=payload, headers=dbl_headers) as dbl_resp:
      logging.info('dbl: posted with code' + str(dbl_resp.status))

async def dbotspw(self):
    headers = {
      'Authorization': config['dbots'],
      'Content-Type': 'application/json'
    }
    payload = json.dumps({
      'server_count': len(self.bot.guilds)
    })
    dbots_url = 'https://bots.discord.pw/api/bots/' + config['botid'] + '/stats'
    async with self.session.post(dbots_url, data=payload, headers=headers) as resp:
      logging.info('dbots: posted with code' + str(resp.status))

  async def listpost():
    if config['dbotsorg'] == False:
      logging.info('not posting to discordbots.org')
    else:
      await dbotsorg()
    if config['dbotspw'] == False:
      logging.info('not posting to bots.discord.pw')
    else:
      await dbotspw()
  def __init__(self, bot):
    self.bot = bot
    self.session = aiohttp.ClientSession(loop=self.bot.loop)
 
  async def on_guild_join( self, guild ):
    logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
    await listpost()

  async def on_guild_remove( self, guild ):
    logging.info('Left ' + str(guild.name))
    await listpost()

def setup(bot):
  bot.add_cog(Stats(bot))
