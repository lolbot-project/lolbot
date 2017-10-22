import random
import urllib.parse

import discord
from discord.ext import commands
import utils.errors
import asyncio
from collections import defaultdict

locks = defaultdict(asyncio.Lock)

class Fun:
    def __init__(self, bot):
        self.bot = bot
        self.headers = None
        # Custom user agent
        self.headers.agent = {
            'User-Agent': 'lolbot(aiohttp/discord.py) - https://lolbot.banne.club'
        }
        # for dad jokes
        self.headers.dadjoke = {
            'User-Agent': self.headers.agent['User-Agent'],
            'Accept': 'text/plain'
        }

    @commands.command()
    async def cat(self, ctx):
        """Random cat images. Awww, so cute! Powered by random.cat"""
        async with self.bot.session.get('https://random.cat/meow', headers=self.headers.agent) as r:
            if r.status == 200:
                js = await r.json()
                em = discord.Embed(name='random.cat', colour=0x690E8)
                em.set_image(url=js['file'])
                await ctx.send(embed=em)
            else:
                raise utils.errors.ServiceError(f'could not fetch cute cat :( (http {r.status})')

    @commands.command()
    async def httpcat(self, ctx, http_id: int):
        """http.cat images - ^httpcat <http code>"""
        codes = [100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 400,
                401, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 414, 416, 417, 418, 420,
                421, 422, 423, 424, 425, 426, 429, 444, 450, 451, 500, 502, 503, 504, 506, 507, 508,
                509, 511, 599]
        if http_id in codes:
            httpcat_em = discord.Embed(name='http.cat', colour=0x690E8)
            httpcat_em.set_image(url=f'https://http.cat/{http_id}.jpg')
            await ctx.send(embed=httpcat_em)
        else:
            raise commands.BadArgument('Specified HTTP code invalid')

    @commands.command()
    async def dog(self, ctx):
        """Random dogs, by random.dog"""
        async with self.bot.session.get('https://random.dog/woof', headers=self.headers.agent) as shibeGet:
            if shibeGet.status == 200:
                shibeImg = await shibeGet.text()
                shibeURL = 'https://random.dog/' + shibeImg
                if '.mp4' in shibeURL:
                    await ctx.send('mp4 file: ' + shibeURL)
                else:
                    shibeEmbed = discord.Embed(colour=0x690E8)
                    shibeEmbed.set_image(url=shibeURL)
                    await ctx.send(embed=shibeEmbed)
            else:
                raise utils.errors.ServiceError(f'could not fetch pupper :( (http {shibeGet.status})')

    @commands.command()
    async def lizard(self, ctx):
        """Shows a random lizard picture"""
        async with self.bot.session.get('https://nekos.life/api/lizard', headers=self.headers.agent) as lizr:
            if lizr.status == 200:
                img = await lizr.json()
                lizEm = discord.Embed(colour=0x690E8)
                lizEm.set_image(url=img['url'])
                await ctx.send(embed=lizEm)
            else:
                raise utils.errors.ServiceError(f'something went boom (http {lizr.status})')

    @commands.command()
    async def why(self, ctx):
        """Why _____?"""
        async with self.bot.session.get('https://nekos.life/api/why', headers=self.headers.agent) as why:
            if why.status == 200:
                whyJS = await why.json()
                whyEm = discord.Embed(title=f'{ctx.author.name} wonders...',
                        description=whyJS['why'], colour=0x690E8)
                await ctx.send(embed=whyEm)
            else:
                raise utils.errors.ServiceError(f'something went boom (http {why.status})')

    @commands.command(aliases=['rhash', 'robothash', 'rh', 'rohash'])
    async def robohash(self, ctx, *, meme: str):
        """Generates a picture of some bot from some text"""
        try:
            e = discord.Embed(colour=0x690E8)
            meme = urllib.parse.quote_plus(meme)
            e.set_image(url=f'https://robohash.org/{meme}.png')
            await ctx.send(embed=e)
        except Exception as e:
            raise utils.errors.ServiceError(f'something broke: {e!s}')

    @commands.command()
    async def k(self, ctx):
        """k"""
        await ctx.send('k')

    @commands.command()
    async def fuck(self, ctx):
        """fuck"""
        await ctx.send('fuck')

    @commands.command(name='8ball')
    async def an8ball(self, ctx, *, question: str):
        pool = ['It is certain', 'Outlook good', 'You may rely on it', 'Ask again '
        'later', 'Concentrate and ask again', 'Reply hazy, try again', 'My reply is '
        'no', 'My sources say no']
        ans = random.choice(pool)
        emb = discord.Embed(title='The Magic 8-ball', description='**Question: ' +
        str(question) + '**\nAnswer: ' + str(ans), colour=0x690E8)
        await ctx.send(embed=emb)

    @commands.command(aliases=['fidget', 'fidgetspinner', 'spinner'])
    async def spin(self, ctx):
        """Spins a fidget spinner!
        The spin time varies from 1 second, to 300 secs (5 mins)."""
        try:
            await locks[ctx.author.id]
            spin_time = random.randint(1, 300)
            land = await ctx.send('You spun a fidget spinner! '
                                  'Let\'s see how long it goes.')
            await asyncio.sleep(spin_time)
            e = discord.Embed(description=f'Your fidget spinner spun for '
                                          f'**{spin_time}** seconds!',
                              colour=0x690E8)
            await land.edit(content='The results are in!', embed=e)
        finally:
            locks[ctx.author.id].release()

    async def get_answer(self, ans: str):
        if ans == 'yes':
            return 'Yes.'
        elif ans == 'no':
            return 'NOPE'
        elif ans == 'maybe':
            return 'maaaaaaybe?'
        else:
            raise commands.BadArgument('internal error: invalid answer lmaoo')

    @commands.command(aliases=['shouldi', 'ask'])
    async def yesno(self, ctx, *, question: str):
        """Why not make your decisions with a bot?"""
        async with ctx.bot.session.get('https://yesno.wtf/api', headers=self.headers.agent) as meme:
            if meme.status == 200:
                mj = await meme.json()
                ans = await self.get_answer(mj['answer'])
                em = discord.Embed(title=ans, colour=0x690E8)
                em.set_image(url=mj['image'])
                await ctx.send(embed=em)
            else:
                raise utils.errors.ServiceError(f'oof (http {meme.status})')

    @commands.command(aliases=['dadjoke', 'awdad', 'dadpls', 'shitjoke', 'badjoke'])
    async def joke(self, ctx):
        """Dad joke simulator 3017, basically"""
        async with ctx.bot.session.get('https://icanhazdadjoke.com', headers=self.headers.dadjoke) as jok:
            if jok.status == 200:
                res = await jok.text()
                await ctx.send(f'`{res}`')
            else:
                raise utils.errors.ServiceError(f'rip dad (http {jok.status})')

def setup(bot):
    bot.add_cog(Fun(bot))
