import sys
import time
import discord
from discord.ext import commands
from random import choice as rchoice
class Utility:
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def uptime(self, ctx):
    """Shows uptime of lolbot"""
    upEm = discord.Embed(title='Uptime', colour=0x690E8)
    startedOn = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(startepoch))
    #timeUp = get_up()
    nowEpoch = time.time()
    upEpoch = nowEpoch - startepoch 
    upEm.add_field(name='Started on', value=startedOn)
    upEm.add_field(name='Uptime', value=time.strftime('%H:%M:%S', time.localtime(upEpoch)))
    try:
      await ctx.send(embed=upEm)
    except Exception as ex:
      await ctx.send('**ERROR** Please report this to lold#1915\n```' + str(ex) + '\n```')

  @commands.command()
  async def stats(self, ctx):
    """A few stats."""
    # get_owner = bot.get_user_info(config['ownerid'])
    statInfo = await ctx.bot.application_info()
    statEmbed = discord.Embed(title='lolbot stats', description='This bot is'
   ' powered by [lolbot](https://github.com/xshotD/lolbot), a fast and powerful '
   'Python bot.', colour=0x690E8)
    statEmbed.add_field(name='Owner', value=statInfo.owner.mention + '('
    + str(statInfo.owner) + ' - ID: ' + str(statInfo.owner.id) + ')')
    statEmbed.add_field(name='Python', value=sys.version)
    statEmbed.add_field(name='discord.py', value=discord.__version__)
    statEmbed.add_field(name='Servers', value=len(bot.guilds))
    statPool = ['What have you done now?', 'Why should I do this again?', 'Oh..',
    'Where did the RAM go?', 'grumble grumble', 'Please hold.', 'No, just, no.',
    'Have you tried rebooting?', 'memework makes the dreamwork!']
    statEmbed.set_footer(text=rchoice(statPool))
    try:
      await ctx.send(embed=statEmbed)
    except:
      await ctx.send('Sorry, I can\'t send the Embed.')
      await ctx.send('Maybe I don\'t have Embed Links permission?')
    else:
      pass

def setup(bot):
  bot.add_cog(Utility(bot))
