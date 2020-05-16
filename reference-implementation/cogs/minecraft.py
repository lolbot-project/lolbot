from discord.ext import commands
from cogs.utils.plainreq import get_req as rq
from discord import Embed
from discord import File
import base64
import codecs


class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mcserver(self, ctx, server: str, port: int = None):
        """Minecraft PC/Bedrock lookup. (Bedrock: use port 19132)"""
        base = "https://api.mcsrvstat.us/2/"
        port = f":{port}" if port else ""
        apiurl = f"{base}{server}{port}"
        async with await rq(ctx.bot.session, apiurl) as r:
            r = await r.json()
            if r["online"]:
                e = Embed(
                    title=f'{server} ({r["version"]})',
                    description="\n".join(r["motd"]["clean"]),
                    colour=0x690E8,
                )
                e.add_field(
                    name="Players",
                    value=f'{r["players"]["online"]}/{r["players"]["max"]}',
                )
                if r.get("software"):
                    e.add_field(name="Server software", value=r["software"])
                if r.get("mods"):
                    e.add_field(name="Mod count", value=len(r["mods"]["names"]))
                if r.get("plugins"):
                    e.add_field(name="Plugin count", value=len(r["plugins"]["names"]))
                if r.get("icon"):
                    with open("/tmp/lolbot-mcicon.png", "wb") as theicon:
                        epic = r["icon"].replace("data:image/png;base64,", "")
                        iconthing = base64.b64decode(epic)
                        theicon.write(iconthing)
                        self.mcfile = File(
                            "/tmp/lolbot-mcicon.png", filename="icon.png"
                        )
                        e.set_thumbnail(url="attachment://icon.png")
                if r.get("icon"):
                    await ctx.send(file=self.mcfile, embed=e)
                else:
                    await ctx.send(embed=e)
            else:
                await ctx.send(
                    embed=Embed(
                        title="Server not online",
                        description="Either the server doesn't exist, or is offline.",
                        colour=0x690E8,
                    )
                )


def setup(bot):
    bot.add_cog(Minecraft(bot))
