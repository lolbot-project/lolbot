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
from random import choice as rchoice
logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
config = json.loads(open('config.json').read())
description = '''beep boop :)'''
bot = commands.AutoShardedBot(command_prefix='^', description=description)
def owneronly(ctx):
  return ctx.message.author.id == '' + config['ownerid']

@bot.command()
async def k(ctx):
  """k"""
  await ctx.send('k')

@bot.command()
async def fuck(ctx):
  """fuck"""
  await ctx.send('fuck')

@bot.command()
async def ping(ctx):
  """Ping? Pong."""
  em = discord.Embed(title='Pong!', description='I am currently alive.', colour=0x690E8)
  em.set_author(name='lolbot')
  await ctx.send(embed=em)

@bot.command()
async def about(ctx):
  """Information about lolbot."""
  em = discord.Embed(title='lolbot', description='Written by lold. (c) 2017 lold, all rights reserved. \nWant to support lolbot and other projects? Donate to my ko-fi (https://ko-fi.com/A753OUG) or PayPal.me (https://paypal.me/ynapw)', colour=0x690E8)
  em.set_author(name='lolbot, written by lold')
  await ctx.send(embed=em)

@bot.command(pass_context=True)
async def suggest( ctx, *, suggestion: str ):
  """Got suggestions?"""
  await ctx.send('Feedback has been forwarded on to the mailbox.')
  await ctx.send(config['sugchannel'], 'Suggestion submitted: `' + str(suggestion) + '`')

@bot.command()
async def cat(ctx):
  """Random cat images. Awww, so cute! Powered by random.cat"""
  with aiohttp.ClientSession() as session:
    async with session.get('https://random.cat/meow') as r:
      if r.status == 200:
        js = await r.json()
        em = discord.Embed(name='random.cat', colour=0x690E8)
        em.set_image(url=js['file'])
        await ctx.send(embed=em)

@bot.command()
async def echo(ctx, *, message: str):
  """Self-explanatory."""
  await ctx.send(message)

@bot.command()
async def httpcat(ctx, *, http_id: str):
  """http.cat images - ^httpcat <http code>"""
  httpcat_em = discord.Embed(name='http.cat', colour=0x690E8)
  httpcat_em.set_image(url='https://http.cat/' + http_id + '.jpg')
  await ctx.send(embed=httpcat_em)

@bot.command(hidden=True, name='eval')
@commands.check(owneronly)
async def evalboi(ctx, *, code: str):
  """Because everyone needs a good eval once in a while."""
  try:
    result = eval(str(code))
  except Exception as e:
    evalError = discord.Embed(title='Error', description='You made non-working code, congrats you fucker.\n**Error:**\n```' + str(result) + ' ```', colour=0x690E8)
    await ctx.send(embed=evalError)
  else:
    evalDone = discord.Embed(title='Eval', description='Okay, I evaluated that for you.\n**Results:**\n```' + str(result) + '```', colour=0x690E8)
    await ctx.send(embed=evalDone)

@bot.command(hidden=True)
@commands.check(owneronly)
async def reboot(ctx):
  """Duh. Owner only"""
  await ctx.send('Second please.')
  logging.info('Restart requested')
  await bot.change_presence(game=discord.Game(name='Restarting'))
  try:
    check_output(['sh', 'bot.sh'])
  except Exception as e:
    await ctx.send('ERROR: fix your fucking code pls')
  else:
    await bot.logout()

@bot.command(hidden=True)
@commands.check(owneronly)
async def game(*, game: str):
  """Changes playing status"""
  await bot.change_presence(game=discord.Game(name=game + ' | ^help | v3.0'))

@bot.command()
async def shibe(ctx):
  """Random shibes, powered by shibe.online"""
  with aiohttp.ClientSession() as shibe:
    async with shibe.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true') as shibeGet:
      if shibeGet.status == 200:
        shibeJson = await shibeGet.json()
        shibeEmbed = discord.Embed(name='shibe.online', colour=0x690E8)
        shibeEmbed.set_image(url=shibeJson[0])
        await ctx.send(embed=shibeEmbed)

@bot.command()
async def stats(ctx):
  """A few stats."""
  get_owner = bot.get_user_info(self.bot.settings.owner)
  statEmbed = discord.Embed(title='lolbot stats', description='This bot is powered by [lolbot](https://github.com/memework/lolbot),'
  ' a fast and powerful Python bot.', colour=0x690E8)
  statEmbed.add_field(name='Owner', value=str(get_owner))
  statEmbed.add_field(name='Python', value=sys.version)
  statEmbed.add_field(name='Servers', value=len(bot.guilds))
  statPool = ['What have you done now?', 'Why should I do this again?', 'Oh..',
  'Where did the RAM go?', 'grumble grumble', 'Please hold.', 'You're fired..',
  'No, please, no.', 'Have you tried rebooting?', 'memework makes the dreamwo'
  'rk']
  statEmbed.set_footer(text=rchoice(statPool))
  await ctx.send(embed=statEmbed)

@bot.command(name='8ball')
async def an8ball(ctx, *, question: str):
  pool = ['It is certain', 'Outlook good', 'You may rely on it', 'Ask again later', 'Concentrate and ask again',
  'Reply hazy, try again', 'My reply is no', 'My sources say no']
  ans = rchoice(pool)
  emb = discord.Embed(title='The Magic 8-ball', description='**Question: ' + str(question) + '**\nAnswer: ' + str(ans), colour=0x690E8)
  await ctx.send(embed=emb)

@bot.event
async def on_guild_join( guild ):
  logging.info('Joined guild ' + str(guild.name))
  logging.info('guild ID ' + str(guild.id))

# danny code frankenstein :P
async def botstats():
  while True:
    async with aiohttp.ClientSession() as session:
      payload = json.dumps({
        'server_count': len(bot.guilds)
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
