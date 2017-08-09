import json
import logging

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
config = json.load(open('config.json'))

class Stats:

    async def dblpost(self):
        headers = {
            'Authorization': self.config['dbl'],
            'Content-Type': 'application/json'
        }
        data = {
            'server_count': len(self.bot.guilds),
            'shard_count': len(self.bot.shards)
        }
        info = await self.bot.application_info()
        req = await self.bot.session.post(f'https://discordbots.org/api/bots/{info.id}/stats', data=json.dumps(data), headers=headers)
        status = req.status
        if status == 200:
            logging.info('poster[dbl]: done')
        else:
            resp = await req.text()
            logging.error(f'poster[dbl]: oops (code {status})')
            logging.error(f'poster[dbl]: response: {resp}')

    async def dpwpost(self):
        headers = {
                'Authorization': self.config['dbots'],
                'Content-Type': 'application/json'
            }
        data = {
                'server_count': len(self.bot.guilds),
                'shard_count': len(self.bot.shards)
            }
        info = await self.bot.application_info()
        req = await self.bot.session.post(f'https://bots.discord.pw/api/bots/{info.id}/stats', data=json.dumps(data), headers=headers)
        status = req.status
        if status == 200:
            logging.info('poster[dbots]: done')
        else:
            resp = await req.text()
            logging.error(f'poster[dbots]: oops (code {status})')
            logging.error(f'poster[dbots]: response: {resp}')

    async def post(self):
        logging.info('poster: starting post')
        await self.dblpost()
        await self.dpwpost()
        logging.info('poster: done')

    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))

    async def on_guild_join( self, guild ):
        logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
        await post()

    async def on_guild_remove( self, guild ):
        logging.info('Left ' + str(guild.name))
        awaitpost()

def setup(bot):
    bot.add_cog(Stats(bot))
