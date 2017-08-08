import json
import logging

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
config = json.load(open('config.json'))

class Stats:

    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))
        self.dbl = dblpost
        self.dpw = dpwpost
        self.post = post

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
        await self.dbl()
        await self.dpw()
        logging.info('poster: done')

    async def on_guild_join( self, guild ):
        logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
        await self.post()

    async def on_guild_remove( self, guild ):
        logging.info('Left ' + str(guild.name))
        await post()

def setup(bot):
    bot.add_cog(Stats(bot))
