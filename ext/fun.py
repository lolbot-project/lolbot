from discord.ext import commands
import discord
import asyncio
from collections import defaultdict
from utils.errors import ServiceError

locks = defaultdict(asyncio.Lock)

class Fun(commands.Cog):
    def __init__(self, bot):
    
    @commands.command()
    async def cat(self, ctx):
        """Random cat images from random.cat"""
        async with ctx.bot.session.get('https://aws.random.cat/meow') as r:
            if r.status == 200:
                json = await r.json()
                embed = discord.Embed(name='A cat', colour=0x690E8)
                embed.set_image(url=json['file'])
                await ctx.send(embed=embed)
            else:
                raise ServiceError(f'request failed, http {r.status}')