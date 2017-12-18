import discord
from cogs import common

class Packages:
    def __init__(self, bot):
        self.bot = bot
        def pkg_url(pkg):
            """Returns the URL for JSON data about a package on PyPI."""
            return f'https://pypi.python.org/pypi/{pkg}/json'

    @commands.command()
    async def pypi(self, ctx, pkg: str):
        async with ctx.bot.session.get(pkg_url(pkg), headers=common.user_agent) as ps:
            pjson = await ps.json()
            pkg_s = discord.Embed(title=f'PyPI stats for {pkg}', colour=0x690E8)
            pkg_s.add_field(name='Version', value=pjson['info']['version'])
            await ctx.send(embed=pkg)
