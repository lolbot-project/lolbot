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
import discord
from discord.ext import commands
from cogs import common

class Packages:
    def __init__(self, bot):
        self.bot = bot

    @classmethod
    def json_pkg(self, pkg):
        """Returns the URL for JSON data about a package on PyPI."""
        return f'https://pypi.python.org/pypi/{pkg}/json'

    @classmethod
    def pkg_url(self, pkg):
        """Returns the URL for a package on PyPI."""
        return f'https://pypi.python.org/pypi/{pkg}'

    @commands.command()
    async def pypi(self, ctx, pkg: str):
        async with ctx.bot.session.get(self.json_pkg(pkg), headers=common.user_agent) as ps:
            pjson = await ps.json()
            pkg_s = discord.Embed(title=pkg, colour=0x690E8)
            pkg_s.add_field(name='Version', value=pjson['info']['version'])
            pkg_s.add_field(name='URL', value=self.pkg_url(pkg))
            await ctx.send(embed=pkg_s)

def setup(bot):
    bot.add_cog(Packages(bot))
