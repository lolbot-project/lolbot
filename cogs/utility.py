import sys
import time
import json
import discord
from discord.ext import commands
from random import choice as rchoice
config = json.load(open('config.json'))
class Utility:
  def __init__(self, bot):
    self.bot = bot
    self.support = 'https://discord.gg/PEW4wx9'

  @commands.command()
  async def uptime(self, ctx):
    """Shows uptime of lolbot"""
    # Thanks Luna you make good code lul
    sec = round(time.time() - self.bot.init_time)
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    upEm = discord.Embed(title='Uptime', colour=0x690E8)
    startedOn = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self.bot.init_time))
    upEm.add_field(name='Started on', value=startedOn + '\n')
    upEm.add_field(name='Uptime', value=f'{d} days, {h} hours, {m} minutes and {s} seconds')
    await ctx.send(embed=upEm)

  @commands.command()
  async def stats(self, ctx):
    """A few stats."""
    # get_owner = bot.get_user_info(config['ownerid'])
    statInfo = await ctx.bot.application_info()
    statEmbed = discord.Embed(title='Stats', description='This bot is'
   ' powered by [lolbot](https://github.com/tilda/lolbot), a fast and powerful '
   'Python bot.', colour=0x690E8)
    statEmbed.add_field(name='Owner', value=statInfo.owner.mention + '('
    + str(statInfo.owner) + ' - ID: ' + str(statInfo.owner.id) + ')')
    statEmbed.add_field(name='Python', value=sys.version)
    statEmbed.add_field(name='discord.py', value=discord.__version__)
    statEmbed.add_field(name='Servers', value=len(self.bot.guilds))
    statPool = ['What have you done now?', 'Why should I do this again?', 'Oh..',
    'Where did the RAM go?', 'grumble grumble', 'Please hold.', 'No, just, no.',
    'Have you tried rebooting?', 'memework makes the dreamwork!']
    statEmbed.set_footer(text=rchoice(statPool))
    await ctx.send(embed=statEmbed)

    @commands.command()
    async def ping(self, ctx):
        """Does exactly what you think it does"""
        before = time.monotonic()
        ping = await ctx.send('ping')
        after = time.monotonic()
        msLogic = round((after - before) * 1000, 2)
        gwLogic = round(self.bot.latency * 1000)
        await ping.edit(content=f'Done: `{msLogic}` (gw: `{gwLogic}`)')

  @commands.command()
  async def invite(self, ctx):
      """Gives a invite for the bot (and also the official server)"""
      info = await ctx.bot.application_info()
      invEmb = discord.Embed(colour=0x690E8)
      invEmb.add_field(name='Invite lolbot', value='[Click here]'
      '(' + discord.utils.oauth_url(info.id) + ')')
      invEmb.add_field(name='Official server', value=str(self.support))
      await ctx.send(embed=invEmb)

def setup(bot):
  bot.add_cog(Utility(bot))
