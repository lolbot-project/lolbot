"""
Owner stuff

Originally made by luna for Jose, the best bot
"""
import os
import traceback
import asyncio
import logging
# noinspection PyPackageRequirements
import discord

# noinspection PyPackageRequirements
from discord.ext import commands

async def run_cmd(cmd: str) -> str:
    """Runs a subprocess and returns the output."""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    results = await process.communicate()
    return "".join(x.decode("utf-8") for x in results)

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def game(self, ctx, *, game: str):
        """Change playing status"""
        haha = ctx.bot.config['prefix']
        try:
            await self.bot.change_presence(
                game=discord.Game(name=f'{game} | {haha}help | v1.1', type=1, url='https://twitch.tv/monstercat'))
        except Exception:
            await ctx.send(f'```\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':white_check_mark: Successfully changed game')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shuts down the bot"""
        await self.bot.session.close()
        await self.bot.logout()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reboot(self, ctx):
        """Reboots the bot.
        Can only be used with PM2"""
        restart_land = discord.Embed(title='Restarting', description='Please wait...')
        restart_msg = await ctx.send(embed=restart_land)
        pm2_id = os.environ.get('pm_id')
        if pm2_id:
            await restart_msg.edit(content='Logging out and restarting. Bye!')
            await self.bot.session.close()
            await self.bot.logout
            await run_cmd(f'pm2 restart {pm2_id}')
        else:
            await restart_message.edit(content=':warning: pm2 not detected, invoking `shutdown` command')
            await ctx.invoke(self.bot.get_command('shutdown'))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *exts: str):
        """Loads a cog"""
        for ext in exts:
            try:
                self.bot.load_extension('cogs.' + extension_name)
            except ModuleNotFoundError:
                await ctx.send(f':x: Cog `{extension_name}` not found.')
                return
            except Exception:
                await ctx.send(f'```py\n{traceback.format_exc()}\n```')
                return
            logging.info(f'owner[load]: cog {extension_name} loaded')
            await ctx.send(f':ok_hand: `{extension_name}` loaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *exts: str):
        """Unloads a cog"""
        for ext in exts:
            self.bot.unload_extension('cogs.' + extension_name)
            logging.info(f'owner[unload]: cog {extension_name} unloaded')
        await ctx.send(f':ok_hand: `{extension_name}` unloaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *exts: str):
        """Reloads a cog"""
        try:
            self.bot.unload_extension('cogs.' + extension_name)
            self.bot.load_extension('cogs.' + extension_name)
        except ModuleNotFoundError:
            await ctx.send(f':x: Cog `{extension_name}` not found.')
            return
        except Exception:
            await ctx.send(f'```{traceback.format_exc()}```')
            return
        logging.info(f'owner[reload]: cog {extension_name} reloaded')
        await ctx.send(f':ok_hand: Reloaded `{extension_name}`')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shell(self, ctx, *, command: str):
        """Run stuff"""
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
        """Lazy much? Whatever..."""
        await ctx.invoke(self.bot.get_command('shell'), command='git pull')


def setup(bot):
    bot.add_cog(Owner(bot))
