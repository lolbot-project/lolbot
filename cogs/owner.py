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

from cogs.utils import haste

async def run_cmd(cmd: str) -> str:
    """Runs a subprocess and returns the output."""
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    results = await process.communicate()
    return "".join(x.decode("utf-8") for x in results)

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(hidden=True)
    @commands.is_owner()
    async def game(self, ctx):
        """Change playing status"""
        if ctx.invoked_subcommand is None:
            _help = discord.Embed(title='Subcommands', colour=0x690E8)
            _help.add_field(name='set', value='Sets playing state. `^game set meme`')
            _help.add_field(name='clear', value='Clears playing state. `^game clear`')
            return await ctx.send(embed=_help)

    @game.command(name='set')
    async def _set(self, ctx, *, game: str):
        """Sets playing state"""
        try:
            await self.bot.change_presence(game=discord.Game(name=f'{game} | {ctx.bot.config["prefix"]}help | v1.2', type=1, url='https://twitch.tv/monstercat'))
        except Exception:
            await ctx.send(f'```\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':white_check_mark: Updated.')

    @game.command(name='clear')
    async def _clear(self, ctx):
        """Resets playing state to normal"""
        try:
            await self.bot.change_presence(game=discord.Game(name=f'{ctx.bot.config["prefix"]}help | v1.2', type=1, url='https://twitch.tv/monstercat'))
        except Exception:
            await ctx.send(f'```\n{traceback.format_exc()}```')
        else:
            await ctx.send(':white_check_mark: Cleared.')

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
        restart_land = discord.Embed(title='Restarting', description='Please wait...', colour=0x690E8)
        restart_msg = await ctx.send(embed=restart_land)
        pm2_id = os.environ.get('pm_id')
        if pm2_id:
            await restart_msg.edit(content='Logging out and restarting. Bye!')
            await self.bot.session.close()
            await self.bot.logout()
            await run_cmd(f'pm2 restart {pm2_id}')
        else:
            await restart_msg.edit(content=':warning: pm2 not detected, invoking `shutdown` command')
            await ctx.invoke(self.bot.get_command('shutdown'))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, *exts: str):
        """Loads a cog"""
        for ext in exts:
            try:
                self.bot.load_extension('cogs.' + ext)
            except ModuleNotFoundError:
                await ctx.send(f':x: Cog `{ext}` not found.')
                return
            except Exception:
                await ctx.send(f'```py\n{traceback.format_exc()}\n```')
                return
            logging.info(f'owner[load]: cog {ext} loaded')
            await ctx.send(f':ok_hand: `{ext}` loaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, *exts: str):
        """Unloads a cog"""
        for ext in exts:
            self.bot.unload_extension('cogs.' + ext)
            logging.info(f'owner[unload]: cog {ext} unloaded')
            await ctx.send(f':ok_hand: `{ext}` unloaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *exts: str):
        """Reloads a cog"""
        for ext in exts:
            try:
                self.bot.unload_extension('cogs.' + ext)
                self.bot.load_extension('cogs.' + ext)
            except ModuleNotFoundError:
                await ctx.send(f':x: Cog `{ext}` not found.')
                return
            except Exception:
                await ctx.send(f'```{traceback.format_exc()}```')
                return
            logging.info(f'owner[reload]: cog {ext} reloaded')
            await ctx.send(f':ok_hand: Reloaded `{ext}`')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shell(self, ctx, *, command: str):
        """Run stuff"""
        with ctx.typing():
            result = await run_cmd(command)
            if len(result) >= 1500:
                paste = await haste(ctx.bot.session, result)
                await ctx.send(f'`{command}`: Too long for Discord! {paste}')
            else:
                await ctx.send(f"`{command}`: ```{result}```\n")

    @commands.command(hidden=True)
    @commands.is_owner()
    async def update(self, ctx):
        """Lazy much? Whatever..."""
        await ctx.invoke(self.bot.get_command('shell'), command='git pull')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def feedbackrespond(self, ctx, p: int, *, res: str):
        with ctx.typing():
            person = ctx.bot.get_user(p)
            fbck = discord.Embed(title='Feedback response', description=res, colour=0x690E8)
            try:
                await person.send(f'Hello {person.name}! The author has responded to your feedback.', embed=fbck)
            except Exception as e:
                return await ctx.send(f'I probably got blocked. ```py\n{e}\n```')
            await ctx.send('Successfully sent response!')

def setup(bot):
    bot.add_cog(Owner(bot))
