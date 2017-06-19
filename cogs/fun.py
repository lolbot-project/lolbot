import discord
from discord.ctx import commands
from random import choice as rchoice
class Fun:
  def __init__(self, bot):
    self.bot = bot
  @commands.command()
  async def cat(self, ctx):
    """Random cat images. Awww, so cute! Powered by random.cat"""
    async with ctx.bot.session.get('https://random.cat/meow') as r:
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
    await ctx.send(embed=httpcat_em)

  @commands.command()
  async def shibe(self, ctx):
    """Random shibes, powered by shibe.online"""
    async with ctx.bot.session.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true') as shibeGet:
      if shibeGet.status == 200:
        shibeJson = await shibeGet.json()
        shibeEmbed = discord.Embed(name='shibe.online', colour=0x690E8)
        shibeEmbed.set_image(url=shibeJson[0])
        await ctx.send(embed=shibeEmbed)
      else:
        await ctx.send('Uh oh, I failed to get the picture for some reason')


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
    ans = rchoice(pool)
    emb = discord.Embed(title='The Magic 8-ball', description='**Question: ' +
    str(question) + '**\nAnswer: ' + str(ans), colour=0x690E8)
    await ctx.send(embed=emb)

def setup(bot):
  bot.add_cog(Fun(bot))
