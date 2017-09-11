import json
import logging
logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
try:
    logging.info('stats[datadog]: initalized')
    from datadog import statsd
except ImportError:
    logging.info('stats[datadog]: datadog not installed')
    logging.info('stats[datadog]: disabling datadog')
    datadog_enabled = False
else:
    logging.info('stats[datadog]: success')
    datadog_enabled = True

class Stats:

    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))

    async def dogpost(self):
        """
        This async function does a post of server and shard count to Datadog.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if datadog_enabled:
            statsd.gauge('servers', len(self.bot.guilds))
            statsd.gauge('shards', len(self.bot.shards))
        else:
            pass

    async def dblpost(self):
        """
        This async function does a post of server and shard count to discordbots.org.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if self.config['dbl'] != "":
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
        else:
            pass

    async def dpwpost(self):
        """
        This async function does a post of server and shard count
        to bots.discord.pw.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if self.config['dbots'] != "":
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
        """
        This async function is a wrapper for dblpost() and dpwpost().
        You shouldn't need to call this yourself, the guild events do this for you.
        """
        logging.info('poster: starting')
        if self.config['dbotsorg']:
            await self.dblpost()
        else:
            pass
        if self.config['dbotspw']:
            await self.dpwpost()
        else:
            pass
        if datadog_enabled:
            await self.dogpost()
        else:
            pass
        logging.info('poster: done')

    async def on_guild_join( self, guild ):
        """
        This async function is called whenever a guild adds a lolbot instance.
        You shouldn't need to call this yourself, discord.py does this automatically.
        """
        logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
        await self.post()

    async def on_guild_remove( self, guild ):
        """
        This async function is called whenever a guild removes a lolbot instance (rip).
        You shouldn't need to call this yourself, discord.py does this automatically.
        """
        logging.info('Left ' + str(guild.name))
        await self.post()

def setup(bot):
    bot.add_cog(Stats(bot))
