from discord.ext import commands
from io import BytesIO, StringIO
from utils.embed import get_embed
from base64 import b64decode
from discord import File

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def pretty_list_info(self, input_list: list, cutoff_length: int=3):
        """
        Pretty-print the list with "and N more"

        Thanks: PythonTryHard (on the Python Discord) for writing this
        """ 
        # Get list length for later usage
        list_length = len(input_list)

        # Main logic
        if cutoff_length > list_length:
            cutoff_list = input_list
            additional_string = ''
        else:
            cutoff_list = input_list[:cutoff_length]
            additional_string = f' and {list_length - cutoff_length} more.'

        # String building
        output_string = ', '.join(cutoff_list) + additional_string
    
        return output_string

    @commands.command()
    async def mcserver(self, ctx, server: str, port: int=None):
        def build_req():
            return f"https://api.mcsrvstat.us/2/{server}{':' + port if port else ''}"

        def player_num(players: dict):
            return f'{players["online"]}/{players["max"]} {"(" + self.pretty_list_info(players["list"]) + ")" if players["online"] > 0 and players.get("list") else ""}'

        async with self.bot.session.get(build_req()) as response:
            embed = get_embed()
            response = await response.json()
            if response["online"] == True:
                embed.description = f'```\n{response["motd"]["clean"][0]}\n```'
                embed.add_field(name="Players", value=player_num(response["players"]))
                if response.get("mods"):
                    embed.add_field(name="Mods", value=self.pretty_list_info(response["mods"]["names"]))
                if response.get("plugins"):
                    embed.add_field(name="Plugins", value=self.pretty_list_info((response["plugins"]["names"])))
                if response.get("icon"):
                    icon = b64decode(response["icon"].replace("data:image/png;base64,", ""))
                    file = File(BytesIO(icon), filename="icon.png")
                    embed.set_thumbnail(url="attachment://icon.png")

            await ctx.send(file=file if response.get("icon") else None, embed=embed)

def setup(bot):
    bot.add_cog(Minecraft(bot))