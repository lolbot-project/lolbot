import json
from discord.ext import commands
import discord

class DBots:
    def __init__(self, bot):
      self.bot = bot
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
       '  `count, info, owner, invite`')

    @dbots.command(name='owner')
    async def dbots_owner(self, ctx, wanted: discord.Member):
        async with self.bot.session.get('https://bots.discord.pw/api/bots/' + str(wanted.id), headers=self.headers) as info:
            """Gets the owner of a bot"""
            if self.config['dbots'] == '':
                await ctx.send('This bot does not have a DBots API key set up.')
            else:
                if info.status == 200:
                    botinfo = await info.json()
                    bot = await self.bot.get_user(botinfo['user_id'])
                    # No multi-owner bot support yet
                    # Because doing that is hard for me tbh
                    owner = await self.bot.get_user(botinfo['owner_ids'][0])
                    ownerbed = discord.Embed(title=f'Who owns {bot.mention}?', description=f'{owner.mention} does!', colour=0x690E8)
                    await ctx.send(embed=ownerbed)
                elif info.status == 404:
                    await ctx.send('That bot is not in Discord Bots!')
                elif info.status == 504:
                    await ctx.send('Server timed out - this is a fault with Discord Bots. Sorry!')

def setup(bot):
  bot.add_cog(DBots(bot))

