# import modules
import logging
import json
import subprocess
import discord

from discord.ext import commands

log = logging.getLogger(__name__)

class Owner:
  def __init__(self, bot):
    self.bot = bot
    self.reporter = self.bot.reporter
    self.config = json.load(open('config.json'))

  @commands.command(hidden=True)
  @commands.is_owner()
  async def reboot(self, ctx):
    """Duh. Owner only"""
    rebootPend = discord.Embed(title='Rebooting', description='Rebooting...', colour=0x690E8)
    await ctx.send(embed=rebootPend)
    try:
      subprocess.check_output(['sh', 'bot.sh'])
      logging.info('reboot requested')
      logging.info('hoping it goes well now')
    except:
      logging.error('pls tell lold to fix his code')
    else:
      await self.bot.logout()

  @commands.command(hidden=True)
  @commands.is_owner()
  async def game(self, ctx, *, game: str):
    """Changes playing status"""
    try:
      await self.bot.change_presence(game=discord.Game(name=game + ' | {}help | v6.2').format(self.config['prefix']))
    except:
      
      await ctx.send('Something went wrong - check the console for details')
    else:
      await ctx.send(':white_check_mark: Changed game')

def setup(bot):
    bot.add_cog(Owner(bot))
