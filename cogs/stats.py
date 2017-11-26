import json
import logging
# noinspection PyPackageRequirements
import discord
from discord.ext import commands

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
try:
    logging.info('stats[datadog]: initalized')
    # noinspection PyPackageRequirements
    from datadog import statsd
except ImportError:
    logging.info('stats[datadog]: datadog not installed')
    logging.info('stats[datadog]: disabling datadog')
    datadog_enabled = False
else:
    logging.info('stats[datadog]: success')
    datadog_enabled = True


async def find_channel(guild):
    """
    Finds a suitable guild channel for posting the
    welcome message. You shouldn't need to call this
    yourself. on_guild_join calls this automatically.

    Thanks FrostLuma for code!
    """
    for c in guild.text_channels:
        if not c.permissions_for(guild.me).send_messages:
            continue
        return c


class Stats:
    def __init__(self, bot):
        self.bot = bot

    async def dogpost(self):
        """
        This async function does a post of server and shard count to Datadog.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if datadog_enabled:
            statsd.gauge('lolbot.servers', len(self.bot.guilds))
            statsd.gauge('lolbot.shards', len(self.bot.shards))
        else:
            pass

    async def dblpost(self):
        """
        This async function does a post of server and shard count to discordbots.org.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if self.bot.config['dbl'] != "":
            headers = {
                'Authorization': self.bot.config['dbl'],
                'Content-Type': 'application/json'
            }
            data = {
                'server_count': len(self.bot.guilds),
                'shard_count': len(self.bot.shards)
            }
            i = await self.bot.application_info()
            req = await self.bot.session.post(f'https://discordbots.org/api/bots/{i.id}/stats',
                                              data=json.dumps(data), headers=headers)
            if req.status == 200:
                logging.info('poster[dbl]: done')
            else:
                t = await req.text()
                logging.error(f'poster[dbl]: oops (code {req.status})')
                logging.error(f'poster[dbl]: response: {t}')
        else:
            pass

    async def dpwpost(self):
        """
        This async function does a post of server and shard count
        to bots.discord.pw.
        You should not have to call this yourself, post() is a wrapper and
        does it for you.
        """
        if self.bot.config['dbots'] != "":
            headers = {
                'Authorization': self.bot.config['dbots'],
                'Content-Type': 'application/json'
            }
            data = {
                'server_count': len(self.bot.guilds),
                'shard_count': len(self.bot.shards)
            }
            i = await self.bot.application_info()
            req = await self.bot.session.post(f'https://bots.discord.pw/api/bots/{i.id}/stats',
                                              data=json.dumps(data), headers=headers)
            status = req.status
            if status == 200:
                logging.info('poster[dbots]: done')
            else:
                resp = await req.text()
                logging.error(f'poster[dbots]: oops (code {status})')
                logging.error(f'poster[dbots]: response: {resp}')

    async def post(self):
        """
        This async function is a wrapper for post functions.
        You shouldn't need to call this yourself, the guild events do this for you.
        """
        if self.bot.config['dbotsorg']:
            await self.dblpost()
        else:
            pass
        if self.bot.config['dbotspw']:
            await self.dpwpost()
        else:
            pass
        if datadog_enabled:
            await self.dogpost()
        else:
            pass

    async def on_guild_join(self, guild):
        """
        This async function is called whenever a guild adds a lolbot instance.
        You shouldn't need to call this yourself, discord.py does this automatically.
        """
        logging.info('Joined guild "' + str(guild.name) + '" ID: ' + str(guild.id))
        welcome_channel = await find_channel(guild)
        we = discord.Embed(title='Hello!',
                           description='Just saying, I may collect information (IDs, etc) about your server'
                           'to help my owner improve the bot. Thanks!', colour=0x690E8)
        we.set_footer(text='Get started by typing ^hello')
        await welcome_channel.send(embed=we)
        await self.post()

    async def on_guild_remove(self, guild):
        """
        This async function is called whenever a guild removes a lolbot instance (rip).
        You shouldn't need to call this yourself, discord.py does this automatically.
        """
        logging.info('Left ' + str(guild.name))
        await self.post()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def poststats(self, ctx):
        """Posts guild stats to bot lists"""
        ok = discord.utils.get(self.bot.emojis, name='check')
        not_ok = discord.utils.get(self.bot.emojis, name='notcheck')
        land = await ctx.send('Hold on a sec...')
        logging.info('poster: forcing post')
        dbl = await ctx.send('Posting to discordbots.org...')
        if self.bot.config['dbotsorg']:
            try:
                await self.dblpost()
            except Exception as e:
                await dbl.edit(content=f'<:notcheck:{not_ok.id}> Error: `\`\`\py\n{e}\n`\`\`')
            else:
                await dbl.edit(content=f'<:check:{ok.id}> Posted to discordbots.org.')
        else:
            await dbl.edit(content='No key configured, skipping discordbots.org!')
        dpw = await ctx.send('Posting to bots.discord.pw...')
        if self.bot.config['dbotspw']:
            try:
                await self.dpwpost()
            except Exception as e:
                await dpw.edit(content=f'<:notcheck:{not_ok.id}> Error: `\`\`\py\n{e}\n`\`\`')
            else:
                await dpw.edit(content=f'<:check:{ok.id}> Posted to bots.discord.pw.')
        else:
            await dpw.edit(content=f'No key configured, skipping bots.discord.pw!')
        ddg = await ctx.send('Posting to Datadog...')
        if datadog_enabled:
            try:
                await self.dogpost()
            except Exception as e:
                await ddg.edit(content=f'<:notcheck:{not_ok.id}> Error: `\`\`\py\n{e}\n`\`\`')
            else:
                await ddg.edit(content=f'<:check:{ok.id}> Posted to Datadog.')
        else:
            await ddg.edit(content='Integration disabled, skipping Datadog!') 
        await land.edit(content='Posted count.')


def setup(bot):
    bot.add_cog(Stats(bot))
