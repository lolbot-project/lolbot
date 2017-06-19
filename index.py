# the lolbot core
# (c) 2017 S Stewart under MIT License

# -*- coding: utf-8 -*-
# obviously, logging
import logging
logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
import json
import aiohttp
import time
try:
  config = json.loads(open('config.json').read())
except:
  logging.debug('Something happened...')
description = '''Just a bot :)'''
exts = ['cogs.donate', 'cogs.fun', 'cogs.owner', 'cogs.stats', 'cogs.utility']
from discord.ext import commands
bot = commands.AutoShardedBot(command_prefix='^', description=description)
bot.session = aiohttp.ClientSession(loop=bot.loop)
bot.startepoch = time.time()
@bot.event
async def on_ready():
  logging.info('lolbot - ready')
  await bot.change_presence(game=discord.Game(name='^help | v6.0'))
  logging.info('Playing status changed')
for ext in exts:
  try:
    bot.load_extension(ext)
  except Exception:
    logging.error('Something happened while loading a cog.')

bot.run(config['token'])

