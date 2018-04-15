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

    @classmethod
    def get_platform(self, platform):
        any_list = ['any', 'UNKNOWN', '']
        if platform in any_list:
            return "Anywhere!"
        else:
            return platform

    @classmethod
    def return_homepage(self, home_page):
        if home_page:
            if 'github.com' in home_page:
                return f'[On GitHub]({home_page})'
            else:
                return f'[Go to site]({home_page})'
        else:
            return 'None.'

    @classmethod
    def summary_ret(self, summary):
        if summary:
            return f'*{summary}*'
        else:
            return '*None.*'

    @commands.command()
    async def pypi(self, ctx, pkg: str):
        async with ctx.bot.session.get(self.json_pkg(pkg),
                                       headers=common.user_agent) as ps:
            if ps.status == 200:
                pkj = await ps.json()
                pkj = pkj['info']
            elif ps.status == 404:
                pkg_s = discord.Embed(title='Error',
                                      description='Package does not exist',
                                      colour=0x690E8)
                return await ctx.send(embed=pkg_s)

            pkg_s = discord.Embed(title=f'{pkg} {pkj["version"]}',
                                  description=self.summary_ret(pkj['summary']),
                                  url=self.pkg_url(pkg),
                                  colour=0x690E8)
            if pkj['home_page']:
                pkg_s.add_field(name='Homepage/Website',
                                value=self.return_homepage(pkj['home_page']))

            pkg_s.add_field(name='License',
                            value=pkj['license'] if pkj['license'] else 'None')

            pkg_s.add_field(name='Platform',
                            value=self.get_platform(pkj['platform']))

            pkg_s.set_footer(text=f'Created by {pkj["author"]}')
            await ctx.send(embed=pkg_s)


def setup(bot):
    bot.add_cog(Packages(bot))
