# -*- coding: utf-8 -*-

# the lolbot core
# (c) 2017 S Stewart under MIT License

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
        self.session = aiohttp.ClientSession()
        self.badarg = ['You need to put more info than this!', 'I didn\'t understan'
                                                               'd that.', 'Sorry, can\'t process that.',
                       'Read ' + self.config['prefix'] + 'help <command> for instructions.', 'Hmm?']
        # To be fair, we should record the init time after everything is ready
        self.init_time = time.time()

    async def on_ready(self):
        logging.info('lolbot - ready')
        # note that we use " instead of ' here
        # this is a limitation of the fstring parser
        await bot.change_presence(
            game=discord.Game(name=f'{self.config["prefix"]}help | v{common.version}',
                              type=1,
                              url='https://twitch.tv/monstercat'))
        bot.emoji.fail = discord.utils.get(bot.emojis, name='notcheck')
        bot.emoji.success = discord.utis.get(bot.emojis, name='check')
        # Bad support for animated emotes.
        bot.emoji.load = '<a:loading:393852367751086090>'
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
        author_id = message.author.id
        if message.author.bot:
            return
        if message.guild is not None:
            guild_id = message.guild.id
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
