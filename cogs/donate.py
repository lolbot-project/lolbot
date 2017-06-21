import discord
from discord.ext import commands

class Donate:
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def donate(self, ctx):
    """Information about lolbot."""
    aboutEm = discord.Embed(description='lolbot is free and I want it to be, but'
                                        ' I need donations to continue this thing.',
                                        colour=0x690E8)
    aboutEm.add_field(name='Patreon', value='https://patreon.com/lold')
    aboutEm.add_field(name='Ko-fi', value='https://ko-fi.com/A753OUG')
    aboutEm.add_field(name='PayPal', value='https://paypal.me/ynapw')
    await ctx.send(embed=aboutEm)

def setup(bot):
  bot.add_cog(Donate(bot))
