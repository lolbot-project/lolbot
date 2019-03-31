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
from cogs.utils.plainreq import get_req


class Packages(commands.Cog):
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
            return 'Any'
        else:
            return platform

    @classmethod
    def return_homepage(self, home_page):
        if home_page:
            if 'github.com' in home_page:
                return f'[On GitHub]({home_page})'
            elif 'gitlab.com' in home_page:
                return f'[On GitLab]({home_page})'
            else:
                return f'[Go to site]({home_page})'
        else:
            return 'None.'

    @classmethod
    def summary_ret(self, summary):
        return f'*{summary}*' if summary else '*None.*'

    @classmethod
    def humanize(self, list):
        return ", and".join(map(str, ", ".join(map(str, list)).rsplit(',', 1)))

    @commands.command()
    async def pypi(self, ctx, pkg: str):
        """Look up a package on the Python Package Index."""
        async with get_req(ctx.bot.session, self.json_pkg(pkg)) as ps:
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

    @commands.command()
    async def crates(self, ctx, pkg: str):
        """Look up a crate on crates.io."""
        async with get_req(ctx.bot.session, 'https://crates.io/api/v1/'
                           f'crates/{pkg}') as ps:
            if ps.status == 200:
                pkj = await ps.json()
                # This API is actually stupid
                pkj_v = pkj['versions']
                pkj = pkj['crate']
            elif ps.status == 404:
                return await ctx.send(embed=discord.Embed(title='Error',
                                      description='Crate does not exist',
                                      colour=0x690E8))
            pkg_s = discord.Embed(title=f'{pkg} {pkj["max_version"]}',
                                  description=self.summary_ret(pkj['description']),
                                  url=f'https://crates.io/crate/{pkg}',
                                  colour=0x690E8)

            if pkj['homepage']:
                pkg_s.add_field(name='Homepage/Website',
                                value=self.return_homepage(pkj['homepage']))

            # Prepare for the worst hack you've ever seen...
            # 3.
            # 2.
            # 1.
            # Ta-da!!!

            the_gay_license = pkj_v[0]['license']
            pkg_s.add_field(name='License',
                            value=the_gay_license)

            pkg_s.add_field(name='Docs',
                            value=pkj['documentation'] if pkj['documentation']
                            else None)
            async with get_req(ctx.bot.session, 'https://crates.io/api/v1/cra'
                               f'tes/{pkg}/owners') as owned:
                owned = await owned.json()
                owned = owned['users']
                owners = []
                for f in owned:
                    owners.append(f['login'])
                pkg_s.set_footer(text=f'Created by {self.humanize(owners)}')
                await ctx.send(embed=pkg_s)


def setup(bot):
    bot.add_cog(Packages(bot))
