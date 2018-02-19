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
# noinspection PyPackageRequirements
#from discord.ext import commands
# noinspection PyPackageRequirements
#import discord


class DBots:
    def __init__(self, bot):
        self.bot = bot
        #self.headers = {
        #    'Authorization': self.config['dbots'],
        #    'Content-Type': 'application/json'
        #}

    #@commands.group()
    #async def dbots(self, ctx):
    #    """Does stuff with bots.discord.pw"""
    #    if ctx.invoked_subcommand is None:
    #        await ctx.send('You must provide a subcommand! Subcommands:'
    #                       '  `count, info, owner, invite`')

    #@dbots.command(name='owner')
    #async def dbots_owner(self, ctx, wanted: discord.Member):
    #    async with self.bot.session.get('https://bots.discord.pw/api/bots/' + str(wanted.id),
    #                                    headers=self.headers) as info:
    #        """Gets the owner of a bot"""
    #        if self.config['dbots'] == '':
    #            await ctx.send('This bot does not have a DBots API key set up.')
    #        else:
    #            if info.status == 200:
    #                botinfo = await info.json()
    #                bot = await self.bot.get_user(botinfo['user_id'])
    #                # No multi-owner bot support yet
    #                # Because doing that is hard for me tbh
    #                owner = await self.bot.get_user(botinfo['owner_ids'][0])
    #                ownerbed = discord.Embed(title=f'Who owns {bot.mention}?', description=f'{owner.mention} does!',
    #                                         colour=0x690E8)
    #                await ctx.send(embed=ownerbed)
    #            elif info.status == 404:
    #                await ctx.send('That bot is not in Discord Bots!')
    #            elif info.status == 504:
    #                await ctx.send('Server timed out - this is a fault with Discord Bots. Sorry!')

def setup(bot):
    bot.add_cog(DBots(bot))
