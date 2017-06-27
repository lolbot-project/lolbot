import json
import logging
import aiohttp

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
config = json.load(open('config.json'))

class Stats:
  # danny code frankenstein :P
  async def botstats(self):
    payload = json.dumps({
      'server_count': len(self.bot.guilds)
    })
    headers = {
      'Authorization': config['dbots'],
      'Content-Type': 'application/json'
    }
    dbl_headers = {
      'Authorization': config['dbl'],
      'Content-Type': 'application/json'
    }
    dbots_url = 'https://bots.discord.pw/api/bots/' + config['botid'] + '/stats'
    dbl_url = 'https://discordbots.org/api/bots/' + config['botid'] + '/stats'
    async with self.session.post(dbl_url, data=payload, headers=dbl_headers) as dbl_resp:
      logging.info('dbl: posted with code' + str(dbl_resp.status))
    async with self.session.post(dbots_url, data=payload, headers=headers) as resp:
      logging.info('dbots: posted with code' + str(resp.status))

  def __init__(self, bot):
    self.bot = bot
    self.session = aiohttp.ClientSession(loop=self.bot.loop)
    self.post = self.botstats
 
  async def on_guild_join( self, guild ):
    logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
    await self.post()

  async def on_guild_remove( self, guild ):
    logging.info('Left ' + str(guild.name))
    await self.post()

def setup(bot):
  bot.add_cog(Stats(bot))
