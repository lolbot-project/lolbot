"""
Owner stuff

Originally made by luna for Jose, the best bot
"""
import traceback
import asyncio
import discord

from discord.ext import commands

class Owner:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def game(self, ctx, *, game: str):
        """Change playing status"""
        haha = ctx.bot.config['prefix']
        try:
            await self.bot.change_presence(game=discord.Game(name=f'{game} | {haha}help | v1.0', type=1, url='https://twitch.tv/monstercat'))
        except Exception:
            await ctx.send(f'```\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(':white_check_mark: Successfully changed game')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send(":wave:")
        await self.bot.session.close()
        await self.bot.logout()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension_name : str):
        """Loads an extension."""
        try:
            self.bot.load_extension('cogs.' + extension_name)
        except ModuleNotFoundError:
            await ctx.send(f':x: Cog `{extension_name}` not found.')
            return
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
            return
        await ctx.send(f':ok_hand: `{extension_name}` loaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, extension_name : str):
        """Unloads an extension."""
        self.bot.unload_extension('cogs.' + extension_name)
        await ctx.send(f':ok_hand: `{extension_name}` unloaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, extension_name : str):
        """Reloads an extension"""
        try:
            self.bot.unload_extension('cogs.' + extension_name)
            self.bot.load_extension('cogs.' + extension_name)
        except ModuleNotFoundError:
            await ctx.send(f':x: Cog `{extension_name}` not found.')
            return
        except Exception:
            await ctx.send(f'```{traceback.format_exc()}```')
            return
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
