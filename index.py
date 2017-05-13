"""
lolbot - by S Stewart
Under MIT License
Copyright (c) S Stewart 2017
"""
# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio
import sys
import logging
import aiohttp
import json
from subprocess import check_output
from other import ownerchecks
from random import choice as rchoice
logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
description = '''beep boop :)'''
bot = commands.Bot(command_prefix='^', description=description)
config = json.loads(open('config.json').read())

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
  em = discord.Embed(title='Pong!', description='I am currently alive.', colour=0x690E8)
  em.set_author(name='lolbot')
  await bot.say(embed=em)

@bot.command()
async def about():
  """Information about lolbot."""
  em = discord.Embed(title='lolbot', description='Written by lold. (c) 2017 lold, all rights reserved.\nDiscord.py version: ' + discord.__version__ + '\nPython version: ' + sys.version + '\nWant to support lolbot and other projects? Donate to my ko-fi (https://ko-fi.com/A753OUG) or PayPal.me (https://paypal.me/ynapw)', colour=0x690E8)
  em.set_author(name='lolbot, written by lold')
  await bot.say(embed=em)

@bot.command(pass_context=True)
async def suggest( ctx, *, suggestion: str ):
  """Got suggestions?"""
  await bot.say('Feedback has been forwarded on to the mailbox.')
  await bot.say(config['sugchannel'], 'Suggestion submitted: `' + str(suggestion) + '`')

@bot.command()
async def cat():
  """Random cat images. Awww, so cute! Powered by random.cat"""
  with aiohttp.ClientSession() as session:
    async with session.get('https://random.cat/meow') as r:
      if r.status == 200:
        js = await r.json()
        em = discord.Embed(name='random.cat', colour=0x690E8)
        em.set_image(url=js['file'])
        await bot.say(embed=em)

@bot.command()
async def echo(*, message: str):
  """Self-explanatory."""
  await bot.say(message)

@bot.command()
async def httpcat(*, http_id: str):
  """http.cat images - ^httpcat <http code>"""
  httpcat_em = discord.Embed(name='http.cat', colour=0x690E8)
  httpcat_em.set_image(url='https://http.cat/' + http_id + '.jpg')
  await bot.say(embed=httpcat_em)

@bot.command(hidden=True, pass_context=True, name='eval')
@ownerchecks.is_owner()
async def evalboi(*, code: str):
  """Because everyone needs a good eval once in a while."""
  try:
    result = eval(str(code))
  except Exception as e:
    evalError = discord.Embed(title='Error', description='You made non-working code, congrats you fucker.\n**Error:**\n```' + str(result) + ' ```', colour=0x690E8)
    await bot.say(embed=evalError)
  else:
    evalDone = discord.Embed(title='Eval', description='Okay, I evaluated that for you.\n**Results:**\n```' + str(result) + '```', colour=0x690E8)
    await bot.say(embed=evalDone)

@bot.command(hidden=True)
@ownerchecks.is_owner()
async def reboot():
  """Duh. Owner only"""
  await bot.say('Second please.')
  logging.info('Restart requested')
  await bot.change_presence(game=discord.Game(name='Restarting'))
  try:
    check_output(['sh', 'bot.sh'])
  except:
    await bot.say('ERROR: fix your fucking code pls')
  else:
    await bot.logout()

@bot.command(hidden=True)
@ownerchecks.is_owner()
async def game(*, game: str):
  """Changes playing status"""
  await bot.change_presence(game=discord.Game(name=game + ' | ^help | v3.0'))

@bot.command()
async def shibe():
  """Random shibes, powered by shibe.online"""
  with aiohttp.ClientSession() as shibe:
    async with shibe.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true') as shibeGet:
      if shibeGet.status == 200:
        shibeJson = await shibeGet.json()
        shibeEmbed = discord.Embed(name='shibe.online', colour=0x690E8)
        shibeEmbed.set_image(url=shibeJson[0])
        await bot.say(embed=shibeEmbed)

@bot.command()
async def stats():
  """A few stats."""
  statEmbed = discord.Embed(title='lolbot stats', description='```\nServers: ' + str(len(bot.servers)) + '\n```', colour=0x690E8)
  await bot.say(embed=statEmbed)

@bot.command(name='8ball')
async def an8ball(*, question: str):
  pool = ['It is certain', 'Outlook good', 'You may rely on it', 'Ask again later', 'Concentrate and ask again', 'Reply hazy, try again', 'My reply is no', 'My sources say no']
  ans = rchoice(pool)
  emb = discord.Embed(title='The Magic 8-ball', description='**Question: ' + str(question) + '**\nAnswer: ' + str(ans), colour=0x690E8)
  await bot.say(embed=emb)

@bot.event
async def on_server_join( server ):
  logging.info('Joined server' + str(server.name))
  logging.info('Server ID' + str(server.id))

# danny code frankenstein :P
async def botstats():
  while True:
    async with aiohttp.ClientSession() as session:
      payload = json.dumps({
        'server_count': len(bot.servers)
      })

      headers = {
        'authorization': config['dbots'],
        'content-type': 'application/json'
      }
      dbl_headers = {
        'authorization': config['dbl'],
        'content-type': 'application/json'
      }

      dbots_url = 'https://bots.discord.pw/api/bots/' + config['botid'] + '/stats'
      dbl_url = 'https://discordbots.org/api/bots/' + config['botid'] + '/stats'
      async with session.post(dbl_url, data=payload, headers=dbl_headers) as dbl_resp:
        logging.info('dbl: posted with code' + str(dbl_resp.status))
      async with session.post(dbots_url, data=payload, headers=headers) as resp:
        logging.info('dbots: posted with code' + str(resp.status))
      await asyncio.sleep(3600) # report to DBL/dbots every hour

try:
  @bot.event
  async def on_ready():
    logging.info('lolbot - ready')
    loop = asyncio.get_event_loop()
    serverpoll = loop.create_task(botstats())
    logging.info('Bot post loop initalized')
    await bot.change_presence(game=discord.Game(name='with APIs. | ^help | v3.0'))
    logging.info('Playing status changed')
except ImportError:
  logging.warn('Module(s) could not be found/not installed')
  logging.warn('Installing automatically')
  check_output(['pip', 'install', '-r', 'requirements.txt'])
  sys.exit('Please relaunch lolbot')

try:
  bot.run(config['token'])
except FileNotFoundError:
  logging.error('I can not find config.json!')
  logging.error('Are you sure you are in the same folder as it?')
