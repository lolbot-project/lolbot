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
from api.server import app as webapp
from hypercorn.asyncio.run import Server
import hypercorn
from ext.common import user_agent

logging.basicConfig(format='(%(asctime)s) [%(levelname)s] - %(message)s', level=logging.INFO)

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except Exception:
    logging.warning('unable to setup uvloop', exc_info=True)

# Thanks: https://github.com/slice/dogbot/blob/master/dog/bot.py#L19
async def _boot_hypercorn(app, config, *, loop):
    socket = config.create_sockets()
    server = await loop.create_server(
        lambda: Server(app, loop, config),
        sock=socket.insecure_sockets[0]
    )
    return server

class Lolbot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config('config.yaml').config
        self.session = aiohttp.ClientSession(loop=self.loop, headers={'User-Agent': user_agent})
        if self.config['api']['enabled']:
            webapp.bot = self
            self.webapp = webapp
            self.http_server = None
            self.http_server_config = hypercorn.Config.from_mapping(self.config['api'])
            self.loop.create_task(self._boot_http_server())
        else:
            logging.info('api disabled, skipping http server boot')

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

    async def _boot_http_server(self):
        try:
            self.http_server = await _boot_hypercorn(self.webapp, self.http_server_config, loop=self.loop)
            logging.info('http server running: %r', self.http_server)
        except Exception:
            logging.exception('http server creation failed')



config = Config('config.yaml').config 
help_command = commands.help.DefaultHelpCommand(dm_help=None)
bot = Lolbot(command_prefix=commands.when_mentioned_or(config['bot']['prefix']),
             description='hi im a bot', help_command=help_command)

if __name__ == '__main__':
    for blahblah, blahblahblah, exts in os.walk('ext'):
        for ext in exts:
            if ext.endswith('.py'):
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