from discord.ext import commands
import discord
import aiohttp

class DBots:
  def __init__(self, bot):
    self.bot = bot
    self.session = aiohttp.ClientSession(loop=self.bot.loop)
    self.config = json.load(open('config.json'))
    self.headers = {
      'Authorization': self.config['dbots'],
      'Content-Type': 'application/json'
    }

  @commands.group()
  async def dbots(self, ctx):
    if ctx.invoked_subcommand is None:
      await ctx.send('You must provide a subcommand! Subcommands:'
      '`count, info, owner, invite`')

  @dbots.command(name='owner')
  async def dbots_owner(self, ctx, wanted: discord.Member):
    async with self.session.get('https://bots.discord.pw/api/bots/' + str(wanted.id), headers=self.headers) as info:
      botinfo = await info.json()
      def getowners():
        owners = json.loads(botinfo['owner_ids'])
        return str(owners)
      await ctx.send('The owner of ' + botinfo['name'] + ' is ' + getowners())

def setup(bot):
  bot.add_cog(DBots(bot))
      
