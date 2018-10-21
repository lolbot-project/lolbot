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
import sys
import time
import datetime
import traceback
# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands
from cogs.owner import run_cmd
from random import choice as rchoice
from cogs.utils import tlist

GitError = 'fatal: Not a git repository (or any of the'
GitError += 'parent directories): .git'
NoCommit = '*No commit'
NoRelease = '*No release*'


def is_bot(u: discord.Member):
    return True if u.bot else False


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
        self.gitlab_url = 'https://gitlab.com/lolbot-project/lolbot'

    @commands.command()
    async def hello(self, ctx):
        """Hey!"""
        hi = "Heya! My name's lolbot. I am a bot designed to do stupid things."
        hi2 = "Things I can do include cat pictures, dog pictures,"
        hi3 = "Wolfram|Alpha, and more!"
        hi4 = "See `^help` for more information on me."
        em = discord.Embed(description=f'{hi} {hi2} {hi3} {hi4}',
                           colour=0x690E8)
        em.add_field(name='Got any questions?',
                     value=f'Join our support server: {self.support}')
        em.set_footer(text='Created by tilda#6729')
        await ctx.send(embed=em)

    @commands.command()
    async def uptime(self, ctx):
        """Shows uptime of lolbot"""
        # Thanks Luna you make good code lul
        uptime_embed = discord.Embed(title='Uptime', colour=0x690E8)
        started_on = time.strftime(
            '%b %d, %Y %H:%M:%S', time.localtime(self.bot.init_time))
        uptime_embed.add_field(
            name='Started on', value=started_on, inline=False)
        meme = bot_uptime(self.bot.init_time)
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
        info = await ctx.bot.application_info()
        statEmbed = discord.Embed(title='Stats',
                                  description='This bot is powered by [lolbot]'
                                              f'({self.gitlab_url}), a fast'
                                              ' and powerful Python bot.',
                                  colour=0x690E8)
        statEmbed.add_field(name='Owner', value=f'{info.owner!s} - ID:'
                                                f' {info.owner.id}')
        statEmbed.add_field(name='Python', value=get_python_version())
        statEmbed.add_field(name='discord.py', value=discord.__version__)
        statEmbed.add_field(name='Servers', value=f'{len(self.bot.guilds)}')
        statEmbed.add_field(name='Uptime',
                            value=bot_uptime(self.bot.init_time))
        statPool = ['What have you done now?', 'Why should I do this again?',
                    'Oh..', 'Where did the RAM go?', 'grumble grumble',
                    'Please hold.', 'No, just, no.',
                    'Have you tried rebooting?',
                    'memework makes the dreamwork!', 'cool and good']
        statEmbed.set_footer(text=rchoice(statPool))
        await ctx.send(embed=statEmbed)

    @commands.command()
    async def invite(self, ctx):
        """Gives a invite for the bot (and also the official server)"""
        invEmb = discord.Embed(colour=0x690E8)
        invEmb.add_field(name='Invite lolbot',
                         value='[Click here](https://lolbot.lmao.tf/invite)')
        invEmb.add_field(name='Official server', value=self.support)
        invEmb.set_footer(
            text='By inviting lolbot, you agree to the lolbot Privacy Policy')
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

        lolbot = '[BOT]' if bot else ''
        e = discord.Embed(title=f'{u.name} {lolbot}',
                          colour=0x690E8)
        e.add_field(name='Name', value=u.name)
        e.add_field(name='Status', value=status)
        e.add_field(name='Joined at', value=join_date)
        e.add_field(name='Joined Discord', value=signup + 'ago')
        e.add_field(name='Currently playing', value=game)
        e.add_field(name='Nickname', value=nick)
        await ctx.send(embed=e)

    @commands.command(aliases=['inviteinfo', 'inv'], hidden=True)
    async def invinfo(self, ctx, code: str):
        """Returns information about a discord.gg invite"""
        await ctx.send('This command is unfinished')

    @commands.command()
    async def version(self, ctx):
        """Returns current version of lolbot"""
        with ctx.typing():
            commit = await run_cmd('git rev-parse --short HEAD')
            e = discord.Embed(colour=0x690E8)
            e.add_field(name='Running commit', value=commit)
            e.add_field(name='Running version', value=ctx.bot.version)
            e.set_footer(text='powered by git (and stuff)!')
            await ctx.send(embed=e)

    @commands.command()
    async def feedback(self, ctx, *, f: str):
        """Have any ideas or comments? Submit them here."""
        with ctx.typing():
            f_channel = ctx.bot.get_channel(ctx.bot.config['feedback'])
            fback = discord.Embed(description=f, colour=0x690E8)
            fback.set_author(name=str(ctx.author),
                             icon_url=ctx.author.avatar_url)
            await f_channel.send(embed=fback)
            await ctx.send('Your feedback was successfully submitted.')

    @commands.command(name='whois')
    async def _whois(self, ctx, domain: str):
        """Looks up a domain using tld list.
        Information may be limited.
        """
        def pick(l):
            if isinstance(l, list):
                return l[0]
            else:
                return l

        def get_status(ctx, res):
            if res['avail']:
                return ctx.bot.emoji.success
            else:
                return ctx.bot.emoji.fail

        def get_premium(res):
            if res['premium']:
                return ':star:'
            else:
                return

        def get_registrar(data):
            r = data['registrarName']
            if r.startswith('TLD Registrar Solutions Ltd'):
                r = 'Internet.bs'
            return r

        domain2 = domain.replace('.', ' ').split(' ')
        subdomain = domain2[0]
        tld = domain2[1]
        data = tlist.construct(subdomain, tld)
        whois_api = tlist.whois_c(domain, ctx.bot.config['whois'])
        async with ctx.bot.session.get(whois_api) as wdata:
            wdata = await wdata.json()
            wdata = wdata['WhoisRecord']
        async with ctx.bot.session.post(tlist.api, headers=tlist.headers,
                                        data=data) as the:
            the = await the.json()
            the = the['result']
            result = the[tld]
            end = discord.Embed(description=f'**{domain}** '
                                f'{get_status(ctx, result)}'
                                f' {get_premium(result) or ""}',
                                colour=0x690E8)
            try:
                try:
                    cre = wdata['createdDate'][:10]
                    exp = wdata['expiresDate'][:10]
                except KeyError:
                    cre = wdata['registryData']['createdDate'][:10]
                    exp = wdata['registryData']['expiresDate'][:10]
                end.add_field(name='Registrar', value=get_registrar(wdata))
                end.add_field(name='Registered', value=cre)
                end.add_field(name='Expiration', value=exp)
            except Exception:
                print(traceback.format_exc())
            await ctx.send(embed=end)

    # @commands.command()
    # async def clean(self, ctx, msgs: int=5):
    #    """Cleans up chat by deleting bot messages.
    #    The default deletion count is 5 messages.
    #    You can delete more by specifying the number as a argument.
    #    Example: ^clean 10
    #    The limit for cleaning is 50, to avoid abuse of the Discord API.
    #    """
    #    load = await ctx.send(f'{ctx.bot.emoji.load!s}'
    #                          ' Cleaning up **{msgs}** messages.')
    #    async for m in ctx.channel.history(limit=50):
    #        for asdfdjfkjfl in range(msgs):
    #            if m.author == ctx.me:
    #                await m.delete()
    #    await load.edit(content=f'{ctx.bot.emoji.check!s}'
    #                    ' Cleaned up **{msgs}** messages.')


def setup(bot):
    bot.add_cog(Etc(bot))
