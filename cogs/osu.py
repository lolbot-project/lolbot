import discord
from discord.ext import commands
from osuapi import OsuApi, AHConnector
import osuapi.enums
import utils.errors

class Osu:
    def __init__(self, bot):
        self.bot = bot
        if bot.config['osu']:
            self.api = OsuApi(bot.config['osu'], connector=AHConnector())
        else:
            self.api = None

    @commands.group()
    async def osu(self, ctx):
        if ctx.invoked_subcommand is None or 'help':
            await ctx.send(embed=discord.Embed(title='Commands for osu!', colour=0x690E8))
                    
    @osu.group()
    async def user(self, ctx, u, mode=osuapi.enums.OsuMode.osu):
        if self.api:
            user = await self.api.get_user(u, mode)
        else:
            raise utils.errors.ServiceError('osu! api key not configured')

def setup(bot):
    bot.add_cog(Osu(bot))
