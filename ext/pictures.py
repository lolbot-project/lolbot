from discord.ext import commands
from utils.embed import get_embed
from random import choice, random
from urllib.parse import quote_plus

class Pictures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quotes = [
            "consider the following: this ",
            "a ",
            "here's a ",
            "have a "
        ]

    def decide_source(self):
        n = random.random()
        if n < 0.5:
            return 'https://random.dog/woof'
        elif n > 0.5:
            return 'https://dog.ceo/api/breeds/image/random'

    def return_rh_set(self, set: str):
        if ['aliens', 'monsters', 'alien', 'monster', 'set2'] in set:
            return 'set2'
        elif ['smoothbrain', 'smooth', 'sexyrobot', 'set3'] in set:
            return 'set3'
        elif ['kitten', 'cat', 'catgirl', 'set4'] in set:
            return 'set4'
        else:
            return None

    @commands.command()
    async def cat(self, ctx):
        """Random cat images from random.cat"""
        async with self.bot.session.get("https://aws.random.cat/meow") as r:
            if r.status == 200:
                r = await r.json()
                embed = get_embed()
                embed.title = choice(self.quotes) + 'cat'
                embed.set_image(url=r['file'])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'random.cat didn\'t send an image. try again later. (http {r.status}')

    @commands.command()
    async def httpcat(self, ctx, http_id: int):
        codes = [
            100,
            101,
            200,
            201,
            202,
            204,
            206,
            207,
            300,
            301,
            302,
            303,
            304,
            305,
            307,
            400,
            401,
            402,
            403,
            404,
            405,
            406,
            408,
            409,
            410,
            411,
            412,
            413,
            414,
            416,
            417,
            418,
            420,
            421,
            422,
            423,
            424,
            425,
            426,
            429,
            444,
            450,
            451,
            500,
            502,
            503,
            504,
            506,
            507,
            508,
            509,
            511,
            599
        ]
        if http_id in codes:
            embed = get_embed()
            embed.title = f'http.cat {http_id!s}'
            embed.set_image(url=f'https://http.cat/{http_id}.jpg')
            await ctx.send(embed=embed)
        else:
            raise commands.BadArgument('Invalid HTTP code')

    @commands.command()
    async def dog(self, ctx):
        async with self.bot.session.get(self.decide_source()) as r:
            if r.status == 200:
                if r.host == 'random.dog':
                    img = await r.text()
                    url = f'https://random.dog/{img}'
                elif r.host == 'dog.ceo':
                    img = await r.json()
                    url = img['message']
                if '.mp4' in url:
                    return await ctx.send(f'video: {url}')
                embed = get_embed()
                embed.set_image(url=url)
                embed.title = choice(self.quotes) + 'dog'
                embed.set_footer(text=f'source: {r.host}')
                await ctx.send(embed=embed)
            else:
                await ctx.send(f'{r.host} didn\'t send back anything. try again later? (http {r.status})')

    @commands.command()
    async def lizard(self, ctx):
        """Random lizard pictures from nekos.life"""
        async with self.bot.session.get('https://nekos.life/api/lizard') as r:
            if r.status == 200:
                r = await r.json()
                embed = get_embed()
                embed.title = choice(self.quotes) + 'lizard'
                embed.set_image(url=r['url'])
            else:
                await ctx.send(f'nekos.life didn\'t send anything back. try again later? (http {r.status})')

    @commands.command(aliases=["rhash", "robothash", "rh", "rohash"])
    async def robohash(self, ctx, *, meme: str, _set: str="set1"):
        if _set != "set1":
            _set = self.return_rh_set(set)
            if _set == None:
                raise commands.BadArgument('Invalid set number/string')
        try:
            embed = get_embed()
            meme = quote_plus(meme)
            embed.set_image(url=f'https://robohash.org/{meme}.png?set={_set}')
            embed.set_footer(text='credit: robohash.org')
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f'u broke it somehow: ```\n{e!s}\n```')

def setup(bot):
    bot.add_cog(Pictures(bot))