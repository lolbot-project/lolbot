from osuapi import OsuApi, AHConnector # osu! api wrapper, with a aiohttp connector (backend)
import discord
from discord.ext import commands

class Osu:
    def __init__(self, bot):
        self.bot = bot
        self.api = OsuApi(bot.config['osu'])

   @commands.group()
   async def osu(self, ctx):
       if ctx.invoked_subcommand is None or 'help':
           osu_embed = discord.Embed(title='Commands for osu!', colour=0x690E8)
           await ctx.send(embed=osu_embed)
           del osu_embed

def setup(bot):
    bot.add_cog(Osu(bot))
