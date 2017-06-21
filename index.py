# the lolbot core
# (c) 2017 S Stewart under MIT License

# -*- coding: utf-8 -*-
# obviously, logging

import json
import logging
import time
import subprocess

import aiohttp
import discord

from discord.ext import commands

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)

try:
  config = json.load(open('config.json'))
except:
  logging.debug('Something happened...')

description = '''Just a bot :)'''

exts = ['donate', 'fun', 'owner', 'stats', 'utility']

bot = commands.AutoShardedBot(command_prefix='^', description=description)
bot.session = aiohttp.ClientSession(loop=bot.loop)

@bot.event
async def on_ready():
  logging.info('lolbot - ready')
  await bot.change_presence(game=discord.Game(name='^help | v6.2'))
  logging.info('Playing status changed')

if __name__ == '__main__':
  for ext in exts:
    try:
      bot.load_extension(f'cogs.{ext}')
    except Exception:
      logging.error(f'Error while loading {ext}', exc_info=True)

  bot.run(config['token'])

