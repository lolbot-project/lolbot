"""
The MIT License (MIT)

Copyright (c) 2018 tilda

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
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
        aboutEm.add_field(name='PayPal', value='Message tilda#6729')
        aboutEm.add_field(name='Other', value='Suggest them, I\'ll consider!')
        await ctx.send(embed=aboutEm)


def setup(bot):
    bot.add_cog(Donate(bot))
