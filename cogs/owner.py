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
    async def shell(self, ctx, *, command: str):
        """Actually running bash commands! Yes, finally!"""
        with ctx.typing():
            p = await asyncio.create_subprocess_shell(command,
                stderr=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
            )

            out, err = map(lambda s: s.decode('utf-8'), await p.communicate())

        result = f'{out}{err}'
        await ctx.send(f"`{command}`: ```{result}```\n")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def update(self, ctx):
        """The laziest way to update your bot."""
        await ctx.invoke(self.bot.get_command('shell'), command='git pull')

def setup(bot):
    bot.add_cog(Owner(bot))
