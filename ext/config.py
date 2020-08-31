from discord.ext import commands
from utils.embed import get_embed
from rich.table import Table
from rich.console import Console
from io import StringIO

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rethink = bot.rethink
        self.conn = bot.db_conn
        self.rich_console = Console(record=True,
                                    color_system=None,
                                    file=StringIO()) # file is StringIO so we can easily access the contents

    @commands.group()
    async def config(self, ctx):
        """
        Set certain options that can be used for commands in lolbot.
        If you need to set server configuration, see the serverconfig command.
        """
        if ctx.invoked_subcommand is None:
            embed = get_embed()
            embed.title = 'lolbot Config'
            embed.description = f"Some lolbot commands support configuration of certain values, like usernames for certain services. If you want to learn more about lolbot's configuration system, see `{ctx.bot.prefix}help config`."
            await ctx.send(embed=embed)

    async def construct_table(self, parts):
        table = Table(show_header=True)
        table.add_column("Property")
        table.add_column("Value")
        async for part in parts:
            table.add_row(part["property"], part["value"])
        self.rich_console.print(table) # Required to "record" the output so we can export it to text
        return self.rich_console.file.getvalue() # Get text from StringIO
        
    @config.command(name='list')
    async def list_all_properties(self, ctx):
        properties = await self.rethink.table("config").filter(self.rethink.row["id"] == ctx.message.author.id).run(self.conn)
        table = await self.construct_table(properties)
        await ctx.send(f'```\n{table}\n```')


    @config.command(name='set')
    async def set_value(self, ctx, property: str, value: str):
        return

def setup(bot):
    bot.add_cog(Config(bot))