import os
import traceback
import asyncio
import logging
from cogs import common
# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands
from cogs.utils import paste
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
"""
Owner stuff

Originally made by luna for Jose, the best bot
"""


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
            _help.add_field(name='set',
                            value='Sets playing state. `^game set meme`')
            _help.add_field(name='clear',
                            value='Clears playing state. `^game clear`')
            return await ctx.send(embed=_help)

    @game.command(name='set')
    async def _set(self, ctx, *, game: str):
        """Sets playing state"""
        try:
            a = discord.Streaming
            g = a(name=f'{game} | {ctx.bot.config["prefix"]}help |'
                       f' v{common.version}',
                  url='https://twitch.tv/monstercat')
            await self.bot.change_presence(activity=g)
        except Exception:
            await ctx.send(f'```\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':white_check_mark: Updated.')

    @game.command(name='clear')
    async def _clear(self, ctx):
        """Resets playing state to normal"""
        try:
            a = discord.Streaming
            p = ctx.bot.config['prefix']
            g = a(name=f'{p}help | v{ctx.bot.version}',
                  url='https://twitch.tv/monstercat')
            await self.bot.change_presence(activity=g)
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
        Can only be used with PM2 or systemd"""
        restart_land = discord.Embed(title='Restarting',
                                     description='Please wait...',
                                     colour=0x690E8)
        re_msg = await ctx.send(embed=restart_land)
        pm2_id = os.environ.get('pm_id')
        if_systemd = os.environ.get('systemd_supervised')
        if pm2_id:
            await re_msg.edit(content='pm2: :wave: bye!')
            await self.bot.session.close()
            await self.bot.logout()
            await run_cmd(f'pm2 restart {pm2_id}')
        elif if_systemd:
            await re_msg.edit(content='systemd: :wave: bye!')
            await self.bot.session.close()
            await run_cmd('systemctl --user restart lolbot')
            await self.bot.logout()
        else:
            await re_msg.edit(content=':warning: No supervisor; invoking'
                              ' `shutdown`')
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
                pa = await paste.haste(ctx.bot.session, result)
                await ctx.send(f'`{command}`: Too long for Discord! {pa}')
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
            try:
                channel = ctx.bot.get_channel(ctx.bot.config['feedback'])
            except Exception:
                await ctx.send(':warning: Cannot find feedback channel?')
            fbck = discord.Embed(title='Feedback response',
                                 description=res, colour=0x690E8)
            try:
                await person.send(f'Hello {person.name}! The owner has '
                                  'responded to your feedback.', embed=fbck)
            except Exception as e:
                return await ctx.send(f'blocked? ```py\n{e}\n```')
            else:
                fbck = discord.Embed(title='Owner response: {str(person)}\'s'
                                           ' feedback',
                                     description=res, colour=0x690E8)
                await channel.send(embed=fbck)
            await ctx.send('Successfully sent response!')


def setup(bot):
    bot.add_cog(Owner(bot))
