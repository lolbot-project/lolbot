# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands


class Donate:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def donate(self, ctx):
        """Support lolbot into the future!"""
        aboutEm = discord.Embed(description='lolbot is a free service. Help me out!',
                                colour=0x690E8)
        aboutEm.add_field(name='Patreon', value='https://patreon.com/lold  ')
        aboutEm.add_field(name='PayPal', value='  https://paypal.me/ynapw')
        await ctx.send(embed=aboutEm)


def setup(bot):
    bot.add_cog(Donate(bot))
