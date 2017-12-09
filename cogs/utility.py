import asyncio
import sys
import time
import json
import datetime
# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands
from cogs import common
from random import choice as rchoice

config = json.load(open('config.json'))
GitError = 'fatal: Not a git repository (or any of the parent directories): .git'
NoCommit = '*No commit'
NoRelease = '*No release*'

def is_bot(u: discord.Member):
    if u.bot:
        return 'Yep!'
    else:
        return 'Nope.'

def get_nick(u: discord.Member):
    if u.nick:
        return u.nick
    else:
        return '*None*'


def get_game_name(u: discord.Member):
    if u.game:
        return u.game.name
    else:
        return '*None*'


def get_join_date(u: discord.Member):
    meme = u.joined_at
    date = meme.strftime('%b %d, %Y %H:%M:%S')
    return date

def delta_str(delta):
   seconds = delta.total_seconds()
   years = seconds / 60 / 60 / 24 / 365.25
   days = seconds / 60 / 60 / 24
   if years >= 1:
       return f'{years:.2f} years'
   else:
       return f'{days:.2f} days'

def get_signup_date(u: discord.Member):
    delta = datetime.datetime.now() - u.created_at
    return delta_str(delta)

def get_status(u: discord.Member):
    if u.status == discord.Status.online:
        return 'Online'
    elif u.status == discord.Status.idle:
        return 'Idle'
    elif u.status == discord.Status.dnd or discord.Status.do_not_disturb:
        return 'Do not disturb'
    elif u.status == discord.Status.offline:
        return 'Offline/invisible'



def get_python_version():
    v = sys.version_info
    return f'{v[0]}.{v[1]}.{v[2]}'

def bot_uptime(init_time):
    sec = round(time.time() - init_time)
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    fmt = f'{d}d{h}h{m}m{s}s'
    if d is 0:
        fmt = f'{h}h{m}m{s}s'
    if h is 0:
        fmt = f'{m}m{s}s'
    if m is 0:
        fmt = f'{s}s'
    if s is 0:
        fmt = '0s'

    return fmt

class Etc:
    def __init__(self, bot):
        self.bot = bot
        self.support = 'https://discord.gg/PEW4wx9'

    @commands.command()
    async def hello(self, ctx):
        """Hey!"""
        hi = "Heya! My name's lolbot. I am a bot designed to do stupid things."
        hi2 = "Things I can do include cat pictures, dog pictures, Wolfram|Alpha"
        hi3 = "and more! See `^help` for more information on me."
        em = discord.Embed(description=f'{hi} {hi2} {hi3}', colour=0x690E8)
        em.add_field(name='Got any questions?', value=f'Join our support server: {self.support}')
        em.set_footer(text='Created by tilda#4778')
        await ctx.send(embed=em)

    @commands.command()
    async def uptime(self, ctx):
        """Shows uptime of lolbot"""
        # Thanks Luna you make good code lul
        uptime_embed = discord.Embed(title='Uptime', colour=0x690E8)
        started_on = time.strftime('%b %d, %Y %H:%M:%S', time.localtime(self.bot.init_time))
        uptime_embed.add_field(name='Started on', value=started_on, inline=False)
        meme = await bot_uptime(self.bot.init_time)
        uptime_embed.add_field(name='Uptime', value=f'{meme}')
        await ctx.send(embed=uptime_embed)

    @commands.command()
    async def ping(self, ctx):
        """Well... you know this"""
        one = time.monotonic()
        a = await ctx.send('wew dude')
        two = time.monotonic()
        ms = round((two - one) * 1000, 2)
        gw = round(self.bot.latency * 1000)
        meme = discord.Embed(title='Pong!', colour=0x690E8)
        meme.add_field(name='Round-trip time', value=f'**{ms}**ms')
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
        statEmbed.add_field(name='Python', value=get_python_version())
        statEmbed.add_field(name='discord.py', value=discord.__version__)
        statEmbed.add_field(name='Servers', value=f'{len(self.bot.guilds)}')
        statEmbed.add_field(name='Uptime', value=bot_uptime(self.bot.init_time))
        statPool = ['What have you done now?', 'Why should I do this again?', 'Oh..',
                    'Where did the RAM go?', 'grumble grumble', 'Please hold.', 'No, just, no.',
                    'Have you tried rebooting?', 'memework makes the dreamwork!', 'cool and good']
        statEmbed.set_footer(text=rchoice(statPool))
        await ctx.send(embed=statEmbed)

    @commands.command()
    async def invite(self, ctx):
        """Gives a invite for the bot (and also the official server)"""
        invEmb = discord.Embed(colour=0x690E8)
        invEmb.add_field(name='Invite lolbot', value='[Click here](https://lolbot.banne.club/invite)')
        invEmb.add_field(name='Official server', value=self.support)
        invEmb.set_footer(text='By inviting lolbot, you agree to the lolbot Privacy Policy')
        await ctx.send(embed=invEmb)

    @commands.command(aliases=['userinfo', 'uinfo'])
    async def user(self, ctx, u: discord.Member):
        try:
            status = get_status(u)
            join_date = get_join_date(u)
            game = get_game_name(u)
            nick = get_nick(u)
            bot = is_bot(u)
            signup = get_signup_date(u)
        except Exception as e:
            raise commands.CommandInvokeError(f'oops: {e}')

        e = discord.Embed(colour=0x690E8)
        e.add_field(name='Name', value=u.name)
        e.add_field(name='Status', value=status)
        e.add_field(name='Joined at', value=join_date)
        e.add_field(name='Joined Discord', value=signup + 'ago')
        e.add_field(name='Currently playing', value=game)
        e.add_field(name='Nickname', value=nick)
        e.add_field(name='Is bot', value=bot)
        await ctx.send(embed=e)

    @commands.command(aliases=['inviteinfo', 'inv'], hidden=True)
    async def invinfo(self, ctx, code: str):
        """Returns information about a discord.gg invite"""
        await ctx.send('This command is unfinished')

    @commands.command()
    async def version(self, ctx):
        """Returns current version of lolbot"""
        with ctx.typing():
            commit = await asyncio.create_subprocess_shell('git log --oneline --abbrev=2',
                                                           stdout=asyncio.subprocess.PIPE,
                                                           stderr=asyncio.subprocess.PIPE)
            co, ce = map(lambda s: s.decode('utf-8'), await commit.communicate())
            if GitError in f'{co}{ce}':
                co = NoCommit
                ce = None
            else:
                pass
            if ce and te is None:
                runVal = '*no release*'
                rVal0 = '*no tag*'
            else:
                runVal = co
                rVal0 = to
            e = discord.Embed(colour=0x690E8)
            e.add_field(name='Latest tag', value=rVal0)
            e.add_field(name='Running version', value=common.version)
            e.set_footer(text='powered by git (and stuff)!')
            await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Etc(bot))
