import json
config = json.loads(open('config.json').read())
import logging
logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
class Stats:
  def __init__(self, bot):
    self.bot = bot
  # danny code frankenstein :P
  async def botstats(self):
    payload = json.dumps({
      'server_count': len(bot.guilds)
    })
    headers = {
      'authorization': config['dbots'],
      'content-type': 'application/json'
    }
    dbl_headers = {
      'authorization': config['dbl'],
      'content-type': 'application/json'
    }
    dbots_url = 'https://bots.discord.pw/api/bots/' + config['botid'] + '/stats'
    dbl_url = 'https://discordbots.org/api/bots/' + config['botid'] + '/stats'
    async with ctx.bot.session.post(dbl_url, data=payload, headers=dbl_headers) as dbl_resp:
      logging.info('dbl: posted with code' + str(dbl_resp.status))
    async with ctx.bot.session.post(dbots_url, data=payload, headers=headers) as resp:
      logging.info('dbots: posted with code' + str(resp.status))

  @bot.event
  async def on_guild_join( self, guild ):
    logging.info('Joined guild ' + str(guild.name) + ' ID: ' + str(guild.id))
    await botstats()

  @bot.event
  async def on_guild_remove( self, guild ):
    logging.info('Left ' + str(guild.name))
    await botstats()

def setup(bot):
  bot.add_cog(Stats(bot))
