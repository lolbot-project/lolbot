from discord.ext import commands
import cogs.utils.ghapi


class GitHub:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gh(self, ctx):
        async with ctx.bot.session.get('https://api.github.com/v3/')
