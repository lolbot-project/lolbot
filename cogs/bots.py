import json
from discord.ext import commands
import discord
import aiohttp

class DBots:
  def __init__(self, bot):
    self.bot = bot
    self.session = aiohttp.ClientSession(loop=self.bot.loop)
    self.config = json.load(open('config.json'))
    self.headers = {
      'Authorization': self.config['dbots'],
      'Content-Type': 'application/json'
    }

  @commands.group()
  async def dbots(self, ctx):
    """Does stuff with bots.discord.pw"""
    if ctx.invoked_subcommand is None:
      await ctx.send('You must provide a subcommand! Subcommands:'
      '`count, info, owner, invite`')

  @dbots.command(name='owner')
  async def dbots_owner(self, ctx, wanted: discord.Member):
    async with self.session.get('https://bots.discord.pw/api/bots/' + str(wanted.id), headers=self.headers) as info:
      """Gets the owner of a bot"""
      if info.status == 200:
        botinfo = await info.json()
        if botinfo['owner_ids'][1] is None:
          owner1 = botinfo['owner_ids'][0]
          await ctx.send(f'The owner {wanted.mention} is {owner1}')
        else:
          if botinfo['owner_ids'][2] is None:
            owner1 = botinfo['owner_ids'][0]
            owner2 = botinfo['owner_ids'][1]
            await ctx.send(f'The owner of {wanted.mention} is {owner1} and {owner2}')
          else:
            owner1 = botinfo['owner_ids'][0]
            owner2 = botinfo['owner_ids'][1]
            owner3 = botinfo['owner_ids'][2]
            await ctx.send(f'The owner of {wanted.mention} is {owner1}, {owner2} and {owner3}')
      elif info.status == 404:
        await ctx.send('That bot is not in Discord Bots!')
      else:
        await ctx.send('A error happened somewhere - sorry about that.')

def setup(bot):
  bot.add_cog(DBots(bot))
      
