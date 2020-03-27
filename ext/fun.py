from discord.ext import commands
import discord
import asyncio
from collections import defaultdict
from utils.errors import ServiceError
import urllib
import random

locks = defaultdict(asyncio.Lock)

class Fun(commands.Cog):
    def __init__(self, bot):
    
    @commands.command()
    async def cat(self, ctx):
        """Random cat images from random.cat"""
        async with ctx.bot.session.get('https://aws.random.cat/meow') as r:
            if r.status == 200:
                json = await r.json()
                embed = discord.Embed(title='a cat', colour=0x690E8)
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
            embed = discord.Embed(title='http.cat', colour=0x690E8)
            embed.set_image(url=f'https://http.cat/{http_id}.jpg')
            await ctx.send(embed=embed)
        else:
            raise commands.BadArgument('Invalid HTTP code')

    @commands.command()
    async def dog(self, ctx):
        """Random dog pictures"""
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
                    embed = discord.Embed(title='a dog', colour=0x690E8)
                    embed.set_image(url=url)
                    embed.set_footer(text=f'from {doggers.host}')
                    await ctx.send(embed=embed)
            else:
                raise ServiceError(f'received http {doggers.status} from host {doggers.host}')

    @commands.command()
    async def lizard(self, ctx):
        """Random lizard pictures"""
        async with self.bot.session.get('https://nekos.life/api/lizard') as l:
            if l.status == 200:
                img = await l.json()
                embed = discord.Embed(title='a lizard', colour=0x690E8)
                embed.set_image(url=img['url'])
                await ctx.send(embed=embed)
            else:
                raise ServiceError(f'host returned http {l.status}')

    @commands.command()
    async def why(self, ctx):
        """Why _____?"""
        async with self.bot.session.get('https://nekos.life/api/why') as w:
            if w.status == 200:
                wot = await w.json()
                embed = discord.Embed(title=f'{ctx.author} wonders...', description=wot['why'], colour=0x690E8)
                await ctx.send(embed=embed)
            else:
                raise ServiceError(f'host returned http {w.status}')

    @commands.command(aliases=['rhash', 'robothash', 'rh', 'rohash'])
    async def robohash(self, ctx, *, meme: str):
        """Turn text into an image of a robot"""
        try:
            embed = discord.Embed(title='robohash', colour=0x690E8)
            yes = urllib.parse.quote_plus(meme)
            embed.set_image(url=f'https://robohash.org/{meme}.png')
            await ctx.send(embed=embed)
        except Exception as e:
            raise ServiceError(f'u broke it: {e!s}')

    @commands.command(aliases=['fidget', 'fidgetspinner', 'spinner'])
    async def spin(self, ctx, override: int=0)
    """Spins a fidget spinner!
    Spin time varies from 1 to 300 seconds."""
    try:
        await locks[ctx.author.id]
        if override is not 0:
            thonk = await ctx.bot.application_info()
            if thonk.owner.id == ctx.message.author.id:
                spin_time = override
            else:
                return await ctx.send('u aren\'t sneaky, u know')
        else:
            spin_time = random.randint(1, 300)
        text = 'You spun a fidget spinner! Let\'s see how long it goes.'
        if spin_time == 1:
            text = 'Oops... You accidentally spun too hard.'
        elif spin_time == 69:
            text = 'You spun a spidget finner! Let\'s see how long it goes.'
        wait = await ctx.send(text)
        await asyncio.sleep(spin_time)
        def find_tx():
            if spin_time == 1:
                return text + '**1 second**'
            elif spin_time == 69:
                return 'Nice time ya got there. **69 seconds**'
            else:
                return f'Cool, you had it spinning for **{spin_time} seconds**.'
        embed = discord.Embed(description=find_tx(), colour=0x690E8)
        await wait.edit(content=f'{ctx.author.mention}', embed=embed)
    finally:
        locks[ctx.author.id].release()

    @commands.command(aliases=['bofh', 'techproblem'])
    async def excuse(self, ctx):
        """Excuses that the Bastard Operator from Hell would use.
        From http://pages.cs.wisc.edu/~ballard/bofh
        """
        async with self.bot.session.get('https://pages.cs.wisc.edu/~ballard/bofh/excuses') as r:
            data = await r.text()
            lines = data.split('\n')
            line = random.choice(lines)
            embed = discord.Embed(description=f'`{line}`', colour=0x690E8)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))