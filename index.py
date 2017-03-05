# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import sys
import logging
import requests
import os
import json
from subprocess import check_output
logging.basicConfig(level=logging.INFO)
description = '''beep boop :)'''
bot = commands.Bot(command_prefix='^', description=description)
try:
  @bot.event
  async def on_ready():
    print('lolbot - ready')
    await bot.change_presence(game=discord.Game(name='with APIs. | ^help | v0.0.1'))
except ImportError:
  logging.error('Please make sure you have all required modules in requirements.txt installed.')
  logging.error('Run this command:')
  logging.error('pip install -r requirements.txt')
  logging.error('to try and fix this error, then relaunch lolbot.')
else:
  print('OK - in check')
@bot.command()
async def k():
  """k"""
  await bot.say('k')

@bot.command()
async def fuck():
  """fuck"""
  await bot.say('fuck')

@bot.command()
async def ping():
  """Ping? Pong."""
  em = discord.Embed(title='Pong!', description='I am currently alive.', colour=0x6906E8)
  em.set_author(name='lolbot', icon_url=bot.user.default_avatar_url)
  await bot.say(embed=em)

@bot.command()
async def about():
  """Information about lolbot."""
  em = discord.Embed(title='lolbot version 0.0.1', description='Written by lold. (c) 2017 lold, all rights reserved.\nDiscord.py version: ' + discord.__version__ + '\nPython version: ' + sys.version + '\nWant to support lolbot and other projects? Donate to my ko-fi (https://ko-fi.com/A753OUG) or PayPal.me (https://paypal.me/ynapw)', colour=0x6906E8)
  em.set_author(name='lolbot, written by lold', icon_url=bot.user.default_avatar_url)
  await bot.say(embed=em)

@bot.command()
async def suggest():
  """Got suggestions?"""
  await bot.say('Suggestions? Direct them to lold#4960 for consideration.')

@bot.command()
async def cat():
  """Random cat images. Awww, so cute! Powered by random.cat"""
  r = requests.get('http://random.cat/meow')
  if r.status_code == 200:
    js = r.json()
    em = discord.Embed(title='lolbot', description='Here is your cat image, as requested.', colour=0x6906E8)
    em.set_author(name='lolbot', icon_url=bot.user.default_avatar_url)
    em.set_image(url=js['file'])
    await bot.say(embed=em)

@bot.command()
async def echo(*, message: str):
  """Self-explanatory."""
  await bot.say(message)

@bot.command()
async def httpcat(*, http_id: str):
  """http.cat images - ^httpcat <http code>"""
  httpcat_em = discord.Embed(title='lolbot', description='http.cat - here is your picture!', colour=0x6906E8)
  httpcat_em.set_image(url='https://http.cat/' + http_id + '.jpg')
  await bot.say(embed=httpcat_em)

@bot.command()
async def changenick(*, user: str, nick: str):
  """^changenick <user> <nick> - needs "Change Nickname" permission"""
  try:
    bot.change_nickname(user, nick)
  except Forbidden:
    logging.warning('Exception: Tried to change nick, Discord has forbidden')
    await bot.say(':x: Tried to change nick, Discord responded with forbidden. Please make sure you have the correct perms for me!')
  except HTTPException:
    logging.warning('Exception: General error: Nickname change failed')
    await bot.say(':x: General error (`HTTPException`): Nick change failed.')
  else:
    await bot.say(':white_check_mark Successfully changed nickname.')
@bot.command()
async def reboot():
  """Duh."""
  await bot.say('Second please.')
  logging.info('Restart requested')
  await bot.change_presence(game=discord.Game(name='Restarting'))
  bot.logout()
  check_output(['python3.6', 'index.py'])
  await bot.change_presence(game=discord.Game('with APIs. | ^help | 0.0.1'))
@bot.command()
async def game(*, game: str):
  """Changes playing status"""
  await bot.change_presence(game=discord.Game(name=game + ' | ^help | v0.0.1'))
config = json.loads(open('config.json').read())
bot.run(config['token'])