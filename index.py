# the lolbot core
# (c) 2017 S Stewart under MIT License

# -*- coding: utf-8 -*-

# built in modules go first.
import json
import logging
import random

# import the rest 

import discord
from discord.ext import commands
from raven import Client

logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)

description = '''Just a bot :)'''
exts = ['bots', 'donate', 'eval', 'fun', 'owner', 'stats', 'utility']

class Lul(commands.AutoShardedBot):
  def __init__(self, *args, **kwargs):
    logging.info('sentry: init')
    super().__init__(*args, **kwargs)
    self.config = json.load(open('config.json'))
    if self.config['sentry']:
      try:
        self.reporter = Client(config['sentryKey'])
      except:
        logging.error('sentry: a error occured - sentry reporting is now disabled.', exc_info=True)
        self.sentryEnabled = False
      else:
        logging.info('sentry: init success, reporting enabled')
        self.sentryEnabled = True
    else:
      self.sentryEnabled = False
       
    self.checkfail = ['heck off', 'You died! [REAL] [Not clickbait]',  'succ my rod', 
    'no u', 'lol no', 'me too thanks', 'are you kidding me', 'kek']
    self.badarg = ['You need to put more info than this!', 'I didn\'t understan'
    'd that.', 'Sorry, can\'t process that.', 
    'Read ' + self.config['prefix'] + 'help <command> for instructions.', 'Hmm?']

  async def on_ready(self):
    logging.info('lolbot - ready')
    # note that we use " instead of ' here
    # this is a limitation of the fstring parser
    await bot.change_presence(game=discord.Game(name=f'{self.config["prefix"]}help | v6.2'))
    logging.info('Playing status changed')

  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
      await ctx.send(f'Permissions error: {random.choice(self.checkfail)}')
    elif isinstance(error, commands.errors.BadArgument):
      await ctx.send(f'Bad argument error: {random.choice(self.badarg)}')
    elif isinstance(error, commands.errors.MissingRequiredArgument):
      await ctx.send(f'Missing argument: {random.choice(self.badarg)}')
    elif isinstance(error, commands.errors.CommandInvokeError):
      if self.config['sentry']:
        self.reporter.captureException()
        await ctx.send('A error occured - sorry! This has been reported.')
      else:
        await ctx.send('A error occured - sorry!')
config = json.load(open('config.json'))
bot = Lul(command_prefix=config['prefix'], description=description)

if __name__ == '__main__':
  for ext in exts:
    try:
      bot.load_extension(f'cogs.{ext}')
    except Exception:
      logging.error(f'Error while loading {ext}', exc_info=True)
    else:
      logging.info(f'Successfully loaded {ext}')

bot.run(config['token'])

