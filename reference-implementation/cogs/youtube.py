import discord
from discord.ext import commands
import urllib.parse
from cogs.utils.plainreq import get_req
import re


class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["yt"])
    async def youtube(self, ctx, *, query: str):
        # First, we get the result that we want
        qs = urllib.parse.urlencode({"search_query": query})
        results = await get_req(
            ctx.bot.session, "https://www.youtube.com/results?" + qs
        )
        video_id = re.findall('href=\\"\\/watch\\?v=(.{11)', await results.text())
        # Fun part!
        # Now we use YouTube Data API to get extra info that normally
        # doesn't get shown in a embed!
        # Actually, not yet. Google can suck my dick with that 0 quota.
        # So for now we'll just send a video link and deal with
        # this shit later!
        print(video_id)
        if len(video_id) < 2:
            return await ctx.send(f"{ctx.bot.emoji.fail} No results found.")
        await ctx.send(f"https://www.youtube.com/watch?v={video_id[0]}")


def setup(bot):
    bot.add_cog(YouTube(bot))
