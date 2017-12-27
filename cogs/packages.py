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
