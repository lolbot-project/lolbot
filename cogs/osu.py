import discord
from discord.ext import commands

class Osu:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def osu(self, ctx):
        await ctx.send(embed=discord.Embed(title='Commands for osu!', colour=0x690E8))

def setup(bot):
    bot.add_cog(Osu(bot))
