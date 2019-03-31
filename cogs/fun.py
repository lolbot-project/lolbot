import random
import urllib.parse

# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands
# noinspection PyPackageRequirements
import utils.errors
import asyncio
from collections import defaultdict
from cogs import common


"""
The MIT License (MIT)

Copyright (c) 2018 tilda

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""


locks = defaultdict(asyncio.Lock)


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.weeb_key = self.bot.config['weeb']
        self.user_agent = {
            'User-Agent': common.user_agent['User-Agent']
        }
        self.weebsh = {
            'User-Agent': common.user_agent['User-Agent'],
            'Authorization': 'Bearer {}'.format(self.weeb_key),
            'Accept': 'application/json'
        }
        self.dadjoke = {
            'User-Agent': common.user_agent['User-Agent'],
            'Accept': 'text/plain'
        }
        self.dbl = {
            'User-Agent': common.user_agent['User-Agent'],
            'Accept': 'application/json'
        }
        self.bb_inv = 'https://discordapp.com/oauth2/authorize'
        self.bb_inv += '?client_id=285480424904327179&scope=bot'

    @commands.command()
    async def cat(self, ctx):
        """Random cat images. Awww, so cute! Powered by random.cat"""
        async with self.bot.session.get('https://aws.random.cat/meow',
                                        headers=self.user_agent) as r:
            if r.status == 200:
                js = await r.json()
                em = discord.Embed(name='random.cat', colour=0x690E8)
                em.set_image(url=js['file'])
                await ctx.send(embed=em)
            else:
                raise utils.errors.ServiceError(f'could not fetch cute cat'
                                                ' :( (http {r.status})')

    @commands.command()
    async def httpcat(self, ctx, http_id: int):
        """http.cat images - ^httpcat <http code>"""
        codes = [100, 101, 200, 201, 202, 204, 206, 207, 300, 301, 302,
                 303, 304, 305, 307, 400, 401, 402, 403, 404, 405, 406,
                 408, 409, 410, 411, 412, 413, 414, 416, 417, 418, 420,
                 421, 422, 423, 424, 425, 426, 429, 444, 450, 451, 500,
                 502, 503, 504, 506, 507, 508, 509, 511, 599]
        if http_id in codes:
            httpcat_em = discord.Embed(name='http.cat', colour=0x690E8)
            httpcat_em.set_image(url=f'https://http.cat/{http_id}.jpg')
            await ctx.send(embed=httpcat_em)
        else:
            raise commands.BadArgument('Specified HTTP code invalid')

    @commands.command()
    async def dog(self, ctx):
        """Random doggos just because!"""
        def decide_source():
            n = random.random()
            if n < 0.5:
                return 'https://random.dog/woof'
            elif n > 0.5:
                return 'https://dog.ceo/api/breeds/image/random'

        async with self.bot.session.get(decide_source(),
                                        headers=self.user_agent) as shibe_get:
            if shibe_get.status == 200:
                if shibe_get.host == 'random.dog':
                    shibe_img = await shibe_get.text()
                    shibe_url = 'https://random.dog/' + shibe_img
                elif shibe_get.host == 'dog.ceo':
                    shibe_img = await shibe_get.json()
                    shibe_url = shibe_img['message']

                if '.mp4' in shibe_url:
                    await ctx.send('video: ' + shibe_url)
                else:
                    shibe_em = discord.Embed(colour=0x690E8)
                    shibe_em.set_image(url=shibe_url)
                    await ctx.send(embed=shibe_em)
            else:
                raise utils.errors.ServiceError(f'could not fetch pupper :('
                                                ' (http {shibe_get.status})')

    @commands.command()
    async def lizard(self, ctx):
        """Shows a random lizard picture"""
        async with self.bot.session.get('https://nekos.life/api/lizard',
                                        headers=self.user_agent) as lizr:
            if lizr.status == 200:
                img = await lizr.json()
                liz_em = discord.Embed(colour=0x690E8)
                liz_em.set_image(url=img['url'])
                await ctx.send(embed=liz_em)
            else:
                raise utils.errors.ServiceError(f'something went boom'
                                                ' (http {lizr.status})')

    @commands.command()
    async def why(self, ctx):
        """Why _____?"""
        async with self.bot.session.get('https://nekos.life/api/why',
                                        headers=self.user_agent) as why:
            if why.status == 200:
                why_js = await why.json()
                why_em = discord.Embed(title=f'{ctx.author.name} wonders...',
                                       description=why_js['why'],
                                       colour=0x690E8)
                await ctx.send(embed=why_em)
            else:
                raise utils.errors.ServiceError(f'something went boom '
                                                '(http {why.status})')

    @commands.command(aliases=['rhash', 'robothash', 'rh', 'rohash'])
    async def robohash(self, ctx, *, meme: str):
        """text => robot image thing"""
        try:
            e = discord.Embed(colour=0x690E8)
            meme = urllib.parse.quote_plus(meme)
            e.set_image(url=f'https://robohash.org/{meme}.png')
            await ctx.send(embed=e)
        except Exception as e:
            raise utils.errors.ServiceError(f'something broke: {e!s}')

        """k"""
        await ctx.send('k')

    @commands.command(name='8ball')
    async def an8ball(self, ctx, *, question: str):
        pool = ['It is certain',
                'Outlook good',
                'You may rely on it',
                'Ask again later',
                'Concentrate and ask again',
                'Reply hazy, try again',
                'My reply is no',
                'My sources say no']
        ans = random.choice(pool)
        emb = discord.Embed(title='The Magic 8-ball',
                            description=f'**Question: {question!s}**'
                            f'\nAnswer: {ans!s}',
                            colour=0x690E8)
        await ctx.send(embed=emb)

    @commands.command(aliases=['fidget', 'fidgetspinner', 'spinner'])
    async def spin(self, ctx, testing: int=0):
        """Spins a fidget spinner!
        The spin time varies from 1 second, to 300 secs (5 mins)."""
        try:
            await locks[ctx.author.id]
            if testing is not 0:
                o = await ctx.bot.application_info()
                if o.owner.id == ctx.message.author.id:
                    spin_time = testing
                else:
                    return await ctx.send('You are not the bot owner.')
            else:
                spin_time = random.randint(1, 300)
            text = 'You spun a fidget spinner! Let\'s see how long it goes.'
            if spin_time == 1:
                text = 'Oops... You accidentally'
                text += ' spun too hard.'
            if spin_time == 69:
                text = 'You spun a spidget finner! Let\'s see how long it goes.'
            land = await ctx.send(text)
            await asyncio.sleep(spin_time)
            def s_tx():
                if spin_time == 1:
                    return 'You spun too hard, whoops. **1 second**'
                elif spin_time == 69:
                    return 'Nice time, huh. **69 seconds**'
                else:
                    return f'Cool, you got a time of **{spin_time}** seconds.'

            await land.edit(content=f'{ctx.author.mention}',
                            embed=discord.Embed(description=s_tx(),
                                                colour=0x690E8))
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
        async with ctx.bot.session.get('https://yesno.wtf/api',
                                       headers=self.user_agent) as meme:
            if meme.status == 200:
                mj = await meme.json()
                ans = await self.get_answer(mj['answer'])
                em = discord.Embed(title=ans,
                                   description='And the answer to'
                                   f' {question} is this',
                                   colour=0x690E8)
                em.set_image(url=mj['image'])
                await ctx.send(embed=em)
            else:
                raise utils.errors.ServiceError(f'oof (http {meme.status})')

    @commands.command(aliases=['dadjoke',
                               'awdad',
                               'dadpls',
                               'shitjoke',
                               'badjoke'])
    async def joke(self, ctx):
        """Dad joke simulator 3017, basically"""
        async with ctx.bot.session.get('https://icanhazdadjoke.com',
                                       headers=self.dadjoke) as jok:
            if jok.status == 200:
                res = await jok.text()
                res = res.encode('utf-8').decode('utf-8')
                await ctx.send(f'`{res}`')
            else:
                raise utils.errors.ServiceError(f'rip dad (http {jok.status})')

    @commands.command(hidden=True)
    async def coolpeople(self, ctx):
        """Displays cool people"""
        if self.bot.config['dbl'] and self.bot.config['dbotsorg']:
            async with ctx.bot.session.get('https://discordbots.org/api/'
                                           f'bots/{ctx.me.id}/votes',
                                           headers=self.dbl) as v:
                e = discord.Embed(title='Upvoters',
                                  description='[Upvote the bot to get here]'
                                  '(https://lolbot.lmao.tf/upvote)!',
                                  colour=0x690E8)
                j = await v.json()
                for l in j:
                    u = []
                    u.append(f'{l["username"]}')
                await ctx.send(u, embed=e)
        else:
            raise utils.errors.ServiceError('dbl key not configured,'
                                            ' see config')

    @commands.command()
    async def sumfuk(self, ctx):
        """U want sum fuk?
        (Thanks weeb.sh)"""
        if self.bot.config['weeb']:
            async with ctx.bot.session.get('https://api.weeb.sh/images/random'
                                           '?type=sumfuk&filetype=png',
                                           headers=self.weebsh) as s:
                if s.status == 200:
                    u = discord.Embed(colour=0x690E8)
                    m = await s.json()
                    f = m['url']
                    u.set_image(url=f)
                    u.set_footer(text='Powered by weeb.sh')
                    # k
                    await ctx.send(embed=u)
                else:
                    raise utils.errors.ServiceError('bird failed '
                                                    f'(http {s.status})')
        else:
            raise utils.errors.ServiceError('weeb.sh key is not configured')

    # @commands.command(aliases=['bird', 'birdpic', 'birbpic'])
    # async def birb(self, ctx):
    #    em = discord.Embed(colour=0x690E8)
    #    em.set_image(url=f'https://random.birb.pw/tweet/random')
    #    await ctx.send(embed=em)

    @commands.command(aliases=['bofh', 'techproblem'])
    async def excuse(self, ctx):
        """Bastard Operator from Hell excuses.
        Source: http://pages.cs.wisc.edu/~ballard/bofh
        """
        async with self.bot.session.get('http://pages.cs.wisc.edu'
                                        '/~ballard/bofh/excuses') as r:
            data = await r.text()
            lines = data.split('\n')
            line = random.choice(lines)
            await ctx.send(f'`{line}`')


def setup(bot):
    bot.add_cog(Fun(bot))
