# the lolbot core
# (c) 2017 S Stewart under MIT License

# -*- coding: utf-8 -*-

# built in modules go first.
import json
import logging
import time
import random

# import the rest 

import aiohttp
import discord

from discord.ext import commands

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)

try:
  config = json.load(open('config.json'))
except:
  logging.debug('Something happened...')

description = '''Just a bot :)'''
checkfail = ['heck off', 'You died! [REAL] [Not clickbait]',  'succ my rod', 
'no u', 'lol no', 'me too thanks', 'are you kidding me', 'kek']
badarg = ['You need to put more info than this!', 'I didn\'t understand that.',
'Sorry, can\'t process that.', 'Read ^help <command> for instructions.', 'Hmm?']
exts = ['donate', 'fun', 'owner', 'stats', 'utility']

bot = commands.AutoShardedBot(command_prefix='^', description=description)

@bot.event
async def on_ready():
  logging.info('lolbot - ready')
  await bot.change_presence(game=discord.Game(name='^help | v6.2'))
  logging.info('Playing status changed')

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.errors.CheckFailure):
      await ctx.send(f'Permissions error: {random.choice(checkfail)}')
  elif isinstance(error, commands.errors.BadArgument):
      await ctx.send(f'Bad argument error: {random.choice(badargs)}')

if __name__ == '__main__':
  for ext in exts:
    try:
      bot.load_extension(f'cogs.{ext}')
    except Exception:
      logging.error(f'Error while loading {ext}', exc_info=True)
    else:
      logging.info(f'Successfully loaded {ext}')

bot.run(config['token'])

