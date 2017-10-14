# -*- coding: utf-8 -*-

# the lolbot core
# (c) 2017 S Stewart under MIT License

import json
import logging
import random
import time
import traceback
import aiohttp
import discord
from discord.ext import commands
import utils.errors

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
description = '''Just a bot :)'''
exts = ['bots', 'donate', 'eval', 'fun', 'nekos', 'owner', 'stats', 'utility', 'weather', 'wa']

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
        await bot.change_presence(game=discord.Game(name=f'{self.config["prefix"]}help | v1.0', type=1, url='https://twitch.tv/monstercat'))
        logging.info('Playing status changed')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.message.add_reaction(ctx.bot.get_emoji(368595774105321472))
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(f'Bad arg: `{random.choice(self.badarg)}`')
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f'Missing argument: {random.choice(self.badarg)}')
        elif isinstance(error, utils.errors.ServiceError):
            logging.error(f'Oops! {error!s}')
            await ctx.message.add_reaction(ctx.bot.get_emoji(368595774105321472))
            await ctx.send(f'Service error: `{err!s}`')
        elif isinstance(error, commands.errors.CommandInvokeError):
            await ctx.message.add_reaction(ctx.bot.get_emoji(368595774105321472))
            tb = ''.join(traceback.format_exception(
                type(error.original), error.original,
                error.original.__traceback__
                ))
            logging.error('A error occured.')
            logging.error(tb)

config = json.load(open('config.json'))
bot = Lul(command_prefix=config['prefix'], description=description, pm_help=True)

if __name__ == '__main__':
    for ext in exts:
        try:
            bot.load_extension(f'cogs.{ext}')
        except Exception:
            logging.error(f'Error while loading {ext}', exc_info=True)
        else:
            logging.info(f'Successfully loaded {ext}')

bot.run(config['token'])
