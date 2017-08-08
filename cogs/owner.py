# import modules
import logging
import json
import subprocess
import discord
import traceback

from discord.ext import commands

log = logging.getLogger(__name__)

class Owner:
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reboot(self, ctx):
        """Duh. Owner only"""
        rebootPend = discord.Embed(title='Rebooting', description='Rebooting...', colour=0x690E8)
        await ctx.send(embed=rebootPend)
        try:
            subprocess.check_output(['./bot.sh'])
            logging.info('reboot requested')
            logging.info('hoping it goes well now')
        except Exception:
            logging.error('A error occured.', exc_info=True)
            logging.error('Please report this error to https://github.com/tilda/lolbot/issues')
        else:
            await self.bot.logout()

  @commands.command(hidden=True)
  @commands.is_owner()
  async def game(self, ctx, *, game: str):
    """Changes playing status"""
    try:
      await self.bot.change_presence(game=discord.Game(name=game + ' | {}help | v6.2').format(self.config['prefix']))
    except Exception:
      logging.error('A error occured.', exc_info=True)
      await ctx.send('Something went wrong - check the console for details')
    else:
      await ctx.send(':white_check_mark: Changed game')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, ext: str):
        pendReload = await ctx.send(f'Attempting to reload *{ext}*...')
        try:
            self.bot.unload_extension(str(ext))
            self.bot.load_extension(str(ext))
        except Exception:
            pendReload.edit(content='... shit. Fix your code! ```\n{traceback.format_exc()}\n```')
        else:
            pendReload.edit(content=f'Reloaded {str(ext)}.')

def setup(bot):
    bot.add_cog(Owner(bot))
