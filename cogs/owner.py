# import modules
import io
import textwrap
import discord
from subprocess import check_output

class Owner:
  @bot.command(hidden=True, name='eval')
  @commands.is_owner()
  async def evalboi(ctx, *, code: str):
    """Because everyone needs a good eval once in a while."""
    # async run code is by sliceofcode (c) sliceofcode 2017
    # env code is (c) Rapptz/Danny 2016
    # the rest is (c) xshotD/S Stewart 2017
    # all of these are under MIT License
    env = {
      'bot': bot,
      'ctx': ctx,
      'message': ctx.message,
      'server': ctx.message.guild,
      'channel': ctx.message.channel,
      'author': ctx.message.author
    }
    env.update(globals())
    try:
      if 'config[\'token\']' in str(code):
        no = discord.Embed(title='No', description='Fuck off you :b:enis', 
        colour=0x690E8)
        await ctx.send(embed=no)
      else:
        stdout = io.StringIO()
        with outredir(stdout):
          wrapped_code = 'async def func():\n' + textwrap.indent(code, '  ')
          lol = exec(compile(code, '<exec>', 'exec'), env)
    except Exception as e:
      evalError = discord.Embed(title='Error', description='You made non-working'
      'code, congrats you fucker.\n**Error:**\n```' + str(e) + ' ```',
       colour=0x690E8)
      await ctx.send(embed=evalError)
    else:
      evalDone = discord.Embed(title='Eval', description='Okay, I evaluated that'
      'for you.\n**Results:**\n```'+ str(stdout.getvalue()) + '```', colour=0x690E8)
      await ctx.send(embed=evalDone)

  @bot.command(hidden=True)
  @commands.is_owner()
  async def reboot(ctx):
    """Duh. Owner only"""
    rebootPend = discord.Embed(title='Rebooting', description='Rebooting...', colour=0x690E7)
    await ctx.send(embed=rebootPend)
    try:
      check_output(['sh', 'bot.sh'])
      logging.info('reboot requested')
      logging.info('hoping it goes well now')
    except:
      logging.error('pls tell lold to fix his code')
    else:
      await bot.logout()

  @bot.command(hidden=True)
  @commands.is_owner()
  async def game(ctx, *, game: str):
    """Changes playing status"""
    try:
      await bot.change_presence(game=discord.Game(name=game + ' | ^help | v6.0'))
    except:
      await ctx.send('Something went wrong - check the console for details')
    else:
      await ctx.send(':white_check_mark: Changed game')

  @bot.command(hidden=True)
  @commands.is_owner()
  async def pull(ctx):
    """Pulls from git then restarts bot."""
    try:
      pullEmb = discord.Embed(title='Pulling from git...', 
      description='Please wait - we are pulling from git.')
      await ctx.end(embed=pullEmb)
      puller = check_output(['git', 'pull', '--rebase'])
    except Exception:
      pullFail = discord.Embed(title='Pull failed',
      description='Check your console for more information.')
    else:
      pullDone = discord.Embed(title='Pulled successfully',
      description='Please reboot the bot with the reboot command.')
      await ctx.send(embed=pullDone)


def setup(bot):
    bot.add_cog(Owner(bot))
