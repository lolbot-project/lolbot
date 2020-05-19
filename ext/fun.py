from discord.ext import commands
import discord
from utils.embed import get_embed
import asyncio
from collections import defaultdict
from utils.errors import ServiceError
import urllib
import random

locks = defaultdict(asyncio.Lock)


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def why(self, ctx):
        """Why _____?"""
        async with self.bot.session.get("https://nekos.life/api/why") as w:
            if w.status == 200:
                wot = await w.json()
                embed = discord.Embed(
                    title=f"{ctx.author} wonders...",
                    description=wot["why"],
                    colour=0x690E8,
                )
                await ctx.send(embed=embed)
            else:
                raise ServiceError(f"host returned http {w.status}")

    @commands.command(aliases=["fidget", "fidgetspinner", "spinner"])
    async def spin(self, ctx, override: int = 0):
        """Spins a fidget spinner!
        Spin time varies from 1 to 300 seconds."""
        try:
            await locks[ctx.author.id]
            if override != 0:
                thonk = await ctx.bot.application_info()
                if thonk.owner.id == ctx.message.author.id:
                    spin_time = override
                else:
                    return await ctx.send("u aren't sneaky, u know")
            else:
                spin_time = random.randint(1, 300)
            text = "You spun a fidget spinner! Let's see how long it goes."
            if spin_time == 1:
                text = "Oops... You accidentally spun too hard."
            elif spin_time == 69:
                text = "You spun a spidget finner! Let's see how long it goes."
            wait = await ctx.send(text)
            await asyncio.sleep(spin_time)

            def find_tx():
                if spin_time == 1:
                    return text + "**1 second**"
                elif spin_time == 69:
                    return "Nice time ya got there. **69 seconds**"
                else:
                    return f"Cool, you had it spinning for **{spin_time} seconds**."

            embed = discord.Embed(description=find_tx(), colour=0x690E8)
            await wait.edit(content=f"{ctx.author.mention}", embed=embed)
        finally:
            locks[ctx.author.id].release()

    @commands.command(aliases=["bofh", "techproblem"])
    async def excuse(self, ctx):
        """Excuses that the Bastard Operator from Hell would use.
        From http://pages.cs.wisc.edu/~ballard/bofh
        """
        async with self.bot.session.get(
            "https://pages.cs.wisc.edu/~ballard/bofh/excuses"
        ) as r:
            data = await r.text()
            lines = data.split("\n")
            line = random.choice(lines)
            embed = discord.Embed(description=f"`{line}`", colour=0x690E8)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
