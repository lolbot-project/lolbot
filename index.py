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
@bot.event
async def on_ready():
	print('lolbot - ready')
	await bot.change_presence(game=discord.Game(name='with APIs. | ^help | v0.0.1'))

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

config = json.loads(open('config.json').read())
bot.run(config['token'])
