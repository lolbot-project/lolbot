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
# -*- coding: utf-8 -*-

from cogs import common
import json
import logging
import random
import time
import traceback
import gc
# noinspection PyPackageRequirements
import aiohttp
# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands
# noinspection PyPackageRequirements
import utils.errors

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
description = '''Just a bot :)'''
exts = ['bots',
        'common',
        'donate',
        'eval',
        'fun',
        'nekos',
        'owner',
        'osu',
        'packages',
        'stats',
        'utility',
        'weather',
        'wa']


class Lul(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = json.load(open('config.json'))

        def prefix_func():
            if self.config['prefix']:
                return self.config['prefix']
            else:
                return '^'  # default
        # Fuck you, PEP8. I hope you are happy
        # because I will send your ass to oblivion
        self.prefix = prefix_func()
        self.ver = common.version
        self.twitch = 'https://twitch.tv/monstercat'
        self.stream = discord.Streaming
        self.session = aiohttp.ClientSession()
        self.badarg = ['You need to put more info than this!',
                       'I didn\'t understand that.',
                       'Sorry, can\'t process that.',
                       f'Read {self.config["prefix"]}help <command>'
                       ' for instructions.',
                       'Hmm?']
        # To be fair, we should record the init time after everything is ready
        self.init_time = time.time()

    async def on_ready(self):
        logging.info('lolbot - ready')
        # note that we use " instead of ' here
        # this is a limitation of the fstring parser
        await bot.change_presence(activity=self.stream(name=f'''{self.prefix}help
                                                            | v{self.ver}''',
                                                       url=self.twitch))
        bot.emoji.fail = discord.utils.get(bot.emojis, name='notcheck')
        bot.emoji.success = discord.utils.get(bot.emojis, name='check')
        bot.emoji.load = discord.utils.get(bot.emojis, name='loading')
        logging.info('Playing status changed')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.message.add_reaction(ctx.bot.emoji.fail)

        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'Bad arg: `{random.choice(self.badarg)}`')

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'Missing argument: {random.choice(self.badarg)}')

        elif isinstance(error, utils.errors.ServiceError):
            tb = ''.join(traceback.format_exception(
                type(error.original), error.original,
                error.original.__traceback__
            ))
            logging.error(f'Oops! {tb}')
            await ctx.message.add_reaction(ctx.bot.emoji.fail)
            await ctx.send(f'Service error: `{tb}`')

        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.message.add_reaction(ctx.bot.emoji.fail)
            tb = ''.join(traceback.format_exception(
                type(error.original), error.original,
                error.original.__traceback__
            ))
            logging.error('A error occured.')
            logging.error(tb)

    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.get_context(message)
        await self.invoke(ctx)


config = json.load(open('config.json'))
bot = Lul(command_prefix=commands.when_mentioned_or(config['prefix']),
          description=description,
          pm_help=None)

if __name__ == '__main__':
    for ext in exts:
        try:
            logging.debug(f'attempting to load {ext}')
            bot.load_extension(f'cogs.{ext}')
        except Exception:
            logging.error(f'Error while loading {ext}', exc_info=True)
        else:
            logging.info(f'Successfully loaded {ext}')

logging.debug('enabling garbage collection')
gc.enable()

logging.debug('starting')
bot.run(config['token'])
