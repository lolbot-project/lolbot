from discord.ext import commands
from utils.embed import get_embed


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        embed = get_embed()
        embed.title = "Hi, I'm lolbot!"
        embed.description = (
            f"I'm a easy to use Discord bot jam packed with features.\n"
            f"If you need any help with my commands, use the `{ctx.bot.prefix}help` command to either view a list of my commands or get information on a specfiic one.\n" 
            f"And if you need any other help with the bot, don't hesitate to join the support server! (See `{ctx.bot.prefix}invite` for the link.)\n Have fun!"
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
