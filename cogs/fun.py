import random

import discord
from discord.ext import commands

class Fun:
  def __init__(self, bot):
    self.bot = bot
    self.ua = {
            'User-Agent': 'lolbot (discord.py/aiohttp)'
        }

  @commands.command()
  async def cat(self, ctx):
    """Random cat images. Awww, so cute! Powered by random.cat"""
    async with self.bot.session.get('https://random.cat/meow', headers=self.ua) as r:
      if r.status == 200:
        js = await r.json()
        em = discord.Embed(name='random.cat', colour=0x690E8)
        em.set_image(url=js['file'])
        await ctx.send(embed=em)

  @commands.command()
  async def httpcat(self, ctx, *, http_id: str):
    """http.cat images - ^httpcat <http code>"""
    httpcat_em = discord.Embed(name='http.cat', colour=0x690E8)
    httpcat_em.set_image(url='https://http.cat/' + http_id + '.jpg')
    httpcat_em.set_footer(text='If there is no image, it doesn\'t exist.')
    await ctx.send(embed=httpcat_em)

  @commands.command()
  async def dog(self, ctx):
    """Random dogs, by random.dog"""
    async with self.bot.session.get('https://random.dog/woof', headers=self.ua) as shibeGet:
        if shibeGet.status == 200:
            shibeImg = await shibeGet.text()
            shibeURL = 'https://random.dog/' + shibeImg
            if '.mp4' in str(shibeURL):
                await ctx.send('mp4 file: ' + shibeURL)
            else:
                shibeEmbed = discord.Embed(colour=0x690E8)
                shibeEmbed.set_image(url=shibeURL)
                await ctx.send(embed=shibeEmbed)
        else:
            await ctx.send(f'Something happened while fetching the picture (HTTP code {shibeGet.status})')

    @commands.command()
    async def lizard(self, ctx):
        """Gets a random lizard"""
        async with self.bot.session.get('https://nekos.life/api/lizard', headers=self.ua) as lizard:
            if lizard.status == 200:
                lizJS = lizard.json()
                lizEm = discord.Embed(colour=0x690E8)
                lizEm.set_image(url=lizJS['lizard'])
                await ctx.send(embed=lizEm)
            else:
                await ctx.send(f'Something happened while fetching the lizard (HTTP code {lizard.status})')

    @commands.command()
    async def why(self, ctx):
        """Why _____?"""
        async with self.bot.session.get('https://nekos.life/api/why', headers=self.ua) as why:
            if why.status == 200:
                whyJS = why.json()
                whyEm = discord.Embed(title=f'{ctx.author.name} wonders...',
                        description=whyJS['why'], colour=0x690E8)
                await ctx.send(embed=whyEm)
            else:
                await ctx.send(f'I wasn\'t able to fetch the sentence. (HTTP code {why.status})')

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

def setup(bot):
    bot.add_cog(Fun(bot))
