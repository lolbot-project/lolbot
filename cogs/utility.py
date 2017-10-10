import asyncio
import sys
import time
import json
import discord
from discord.ext import commands
from random import choice as rchoice

config = json.load(open('config.json'))
GitError = 'fatal: Not a git repository (or any of the parent directories): .git'

class Etc:
    def __init__(self, bot):
        self.bot = bot
        self.support = 'https://discord.gg/PEW4wx9'

    @commands.command()
    async def uptime(self, ctx):
        """Shows uptime of lolbot"""
        # Thanks Luna you make good code lul
        sec = round(time.time() - self.bot.init_time)
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        upEm = discord.Embed(title='Uptime', colour=0x690E8)
        startedOn = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self.bot.init_time))
        upEm.add_field(name='Started on', value=startedOn + '\n |')
        upEm.add_field(name='Uptime', value=f' {d} days, {h} hours, {m} minutes and {s} seconds')
        await ctx.send(embed=upEm)

    @commands.command()
    async def ping(self, ctx):
        """Well... you know this"""
        one = time.monotonic()
        a = await ctx.send('wew dude')
        two = time.monotonic()
        ms = round((two - one) * 1000, 2)
        gw = round(self.bot.latency * 1000)
        meme = discord.Embed(title='Pong!', colour=0x690E8)
        meme.add_field(name='Normal ping', value=f'**{ms}**ms')
        meme.add_field(name='Gateway ping', value=f'**{gw}**ms')
        await a.delete()
        await ctx.send(embed=meme)

    @commands.command()
    async def stats(self, ctx):
        """A few stats."""
        statInfo = await ctx.bot.application_info()
        statEmbed = discord.Embed(title='Stats', description='This bot is'
        ' powered by [lolbot](https://github.com/tilda/lolbot), a fast and powerful '
        'Python bot.', colour=0x690E8)
        statEmbed.add_field(name='Owner', value=statInfo.owner.mention + '('
        + str(statInfo.owner) + ' - ID: ' + str(statInfo.owner.id) + ')')
        statEmbed.add_field(name='Python', value=sys.version)
        statEmbed.add_field(name='discord.py', value=discord.__version__)
        statEmbed.add_field(name='Servers', value=len(self.bot.guilds))
        statPool = ['What have you done now?', 'Why should I do this again?', 'Oh..',
                'Where did the RAM go?', 'grumble grumble', 'Please hold.', 'No, just, no.',
                'Have you tried rebooting?', 'memework makes the dreamwork!']
        statEmbed.set_footer(text=rchoice(statPool))
        await ctx.send(embed=statEmbed)

    @commands.command()
    async def invite(self, ctx):
        """Gives a invite for the bot (and also the official server)"""
        info = await ctx.bot.application_info()
        invEmb = discord.Embed(colour=0x690E8)
        invEmb.add_field(name='Invite lolbot', value='[Click here]'
                '(' + discord.utils.oauth_url(info.id) + ')')
        invEmb.add_field(name='Official server', value=str(self.support))
        await ctx.send(embed=invEmb)

    @commands.command()
    async def version(self, ctx):
        """Returns current version of lolbot"""
        with ctx.typing():
            tag = await asyncio.create_subprocess_shell('git describe --abbrev=0 --tags',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE)
            commit = await asyncio.create_subprocess_shell('git log --oneline --abbrev=2',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE)
            co, ce = map(lambda s: s.decode('utf-8'), await commit.communicate())
            to, te = map(lambda st: st.decode('utf-8'), await tag.communicate())
            if f'{co}{ce}' == GitError:
                co, ce = '*No commit*'
            else:
                pass
            if f'{to}{te}' == GitError:
                to, te = '*No release*'
            else:
                pass
            e = discord.Embed(colour=0x690E8)
            e.add_field(name='Latest tag', value=f'{to}{te}')
            e.add_field(name='Currently running', value=f'git-{co}{ce}')
            e.set_footer(text='powered by git (and stuff)!')
            await ctx.send(embed=e)


def setup(bot):
  bot.add_cog(Etc(bot))
