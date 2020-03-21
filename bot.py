"""
lolbot rewrite - (c) 2020 tilda under MIT License

This module contains code needed to start the bot, including other services such as the API
"""

import discord
from discord.ext import commands
import logging
from utils.prefix import get_prefix
from utils.version import get_version
from utils.config import Config
import time
import os
import aiohttp
import asyncio

logging.basicConfig(format='(%(asctime)s) [%(levelname)s] - %(message)s', level=20)

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    logging.warning('unable to setup uvloop', exc_info=True)

class Lolbot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.config = Config('config.yaml').config
        except Exception:
            logging.error('Loading YAML failed. Does the file exist, and is it valid?', exc_info=True)
        self.session = aiohttp.ClientSession()

    async def on_ready(self):
        logging.info('lolbot has started up')
        await bot.change_presence(activity=discord.Streaming(
            name=f'{get_prefix(self.config)}help | v{get_version()}',
            url='https://twitch.tv/monstercat'))
        self.init_time = time.time()

    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.get_context(message)
        await self.invoke(ctx)


config = Config('config.yaml').config 
help_command = commands.help.DefaultHelpCommand(dm_help=None)
bot = Lolbot(command_prefix=commands.when_mentioned_or(config['bot']['prefix']),
             description='hi im a bot', help_command=help_command)

if __name__ == '__main__':
    for blahblah, blahblahblah, exts in os.walk('ext'):
        for ext in exts:
            try:
                logging.info(f'attempting to load {ext}')
                ext = ext.replace('.py', '') 
                bot.load_extension(f'ext.{ext}')
            except Exception:
                logging.error(f'failed to load {ext}', exc_info=True)
            else:
                logging.info(f'successfully loaded {ext}')
    logging.info('loading jishaku')
    bot.load_extension('jishaku')

bot.run(config['tokens']['discord'])