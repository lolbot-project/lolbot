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

    @commands.command()
    async def httpcat(self, ctx, http_id: int):
        codes = [100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302,
                 303, 304, 305, 307, 400, 401, 402, 403, 404, 405, 406,
                 408, 409, 410, 411, 412, 413, 414, 416, 417, 418, 420,
                 421, 422, 423, 424, 425, 426, 429, 444, 450, 451, 500,
                 502, 503, 504, 506, 507, 508, 509, 511, 599]
        if http_id in codes:
            embed = discord.Embed(name='http.cat', colour=0x690E8)
            embed.set_image(url=f'https://http.cat/{http_id}.jpg')
            await ctx.send(embed=embed)
        else:
            raise commands.BadArgument('Invalid HTTP code')

    @commands.command()
    async def dog(self, ctx):
        def decide_source():
            n = random.random()
            if n < 0.5:
                return 'https://random.dog/woof'
            elif n > 0.5:
                return 'https://dog.ceo/api/breeds/image/random'

        async with self.bot.session.get(decide_source()) as doggers:
            if doggers.status == 200:
                if doggers.host == 'random.dog':
                    img = await doggers.text()
                    url = f'https://random.dog/{img}'
                elif doggers.host == 'dog.ceo':
                    img = await doggers.json()
                    url = img['message']
                if '.mp4' in url:
                    await ctx.send(f'video: {url}')
                else:
                    embed = discord.Embed(name='a dog', colour=0x690E8)
                    embed.set_image(url=url)
                    embed.set_footer(text=f'from {doggers.host}')
                    await ctx.send(embed=embed)
            else:
                raise ServiceError(f'received http {doggers.status} from host {doggers.host}')

