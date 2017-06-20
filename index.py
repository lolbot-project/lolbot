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
import discord
from discord.ext import commands
bot = commands.AutoShardedBot(command_prefix='^', description=description)
bot.session = aiohttp.ClientSession(loop=bot.loop)

@bot.command(hidden=True)
@commands.is_owner()
async def reboot(ctx):
  """Duh. Owner only"""
  rebootPend = discord.Embed(title='Rebooting', description='Rebooting...', colour=0x690E7)
  await ctx.send(embed=rebootPend)
  try:
    check_output(['sh', 'bot.sh'])
    logging.info('reboot requested')
    logging.info('hoping it goes well now')
  except:
    logging.error('pls tell lold to fix his code')
  else:
    await bot.logout()

@bot.command(hidden=True)
@commands.is_owner()
async def game(ctx, *, game: str):
  """Changes playing status"""
  try:
     await bot.change_presence(game=discord.Game(name=game + ' | ^help | v6.1'))
  except:
    await ctx.send('Something went wrong - check the console for details')
  else:
    await ctx.send(':white_check_mark: Changed game')

@bot.event
async def on_ready():
  logging.info('lolbot - ready')
  await bot.change_presence(game=discord.Game(name='^help | v6.1'))
  logging.info('Playing status changed')
for ext in exts:
  try:
    bot.load_extension(ext)
  except Exception:
    logging.debug('Something happened while loading a cog.')

bot.run(config['token'])

