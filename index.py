# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio
import sys
import logging
import aiohttp
import json
import textwrap
from subprocess import check_output
from other import ownerchecks

logging.basicConfig(level=logging.INFO)
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
  em = discord.Embed(title='Pong!', description='I am currently alive.', colour=0x6906E8)
  em.set_author(name='lolbot', icon_url=bot.user.default_avatar_url)
  await bot.say(embed=em)

@bot.command()
async def about():
  """Information about lolbot."""
  em = discord.Embed(title='lolbot version 1.0', description='Written by lold. (c) 2017 lold, all rights reserved.\nDiscord.py version: ' + discord.__version__ + '\nPython version: ' + sys.version + '\nWant to support lolbot and other projects? Donate to my ko-fi (https://ko-fi.com/A753OUG) or PayPal.me (https://paypal.me/ynapw)', colour=0x6906E8)
  em.set_author(name='lolbot, written by lold', icon_url=bot.user.default_avatar_url)
  await bot.say(embed=em)

@bot.command(pass_context=True)
async def suggest( ctx, *, suggestion: str ):
  """Got suggestions?"""
  await bot.say('Feedback has been forwarded on to the mailbox.')
  await bot.say(config['sugchannel'], 'Suggestion submitted: `' + str(suggestion) + '`')

@bot.command()
async def cat():
  with aiohttp.ClientSession() as session:
    """Random cat images. Awww, so cute! Powered by random.cat"""
    async with session.get('https://random.cat/meow') as r:
      if r.status == 200:
        js = await r.json()
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

# slice's eval code :^)
@bot.command(hidden=True, pass_context=True)
@ownerchecks.is_owner()
async def eval(self, ctx, *, code: str):
  """Because everyone needs a good eval once in a while."""
  env = {
    'bot': ctx.bot,
    'ctx': ctx,
    'msg': ctx.message,
    'guild': ctx.guild,
    'channel': ctx.channel,
    'me': ctx.message.author,
    'get': discord.utils.get,
    'find': discord.utils.find,
  }

  fmt_exception = '```py\n>>> {}\n\n{}: {}```'

  env.update(globals())

  indented_code = textwrap.indent(code, '    ')
  wrapped_code = 'async def _eval_code():\n' + indented_code
  try:
      exec(wrapped_code, env)
      return_value = await env['_eval_code']()
      if return_value is not None:
        await ctx.send(return_value)
  except Exception as e:
      name = type(e).__name__
      await ctx.send(fmt_exception.format(code, name, e))
      return
@bot.command(hidden=True)
@ownerchecks.is_owner()
async def reboot():
  """Duh. Owner only"""
  await bot.say('Second please.')
  logging.info('Restart requested')
  await bot.change_presence(game=discord.Game(name='Restarting'))
  check_output(['sh', 'bot.sh'])
  await bot.logout()

@bot.command(hidden=True)
@ownerchecks.is_owner()
async def game(*, game: str):
  """Changes playing status"""
  await bot.change_presence(game=discord.Game(name=game + ' | ^help | v2.0'))

@bot.command()
async def shibe():
  with aiohttp.ClientSession() as shibe:
    """Random shibes, powered by shibe.online"""
    async with shibe.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true') as shibeGet:
      if shibeGet.status == 200:
        shibeJson = await shibeGet.json()
        shibeEmbed = discord.Embed(name='shibe.online', colour=0x6906E8)
        shibeEmbed.set_image(url=shibeJson[0])
        await bot.say(embed=shibeEmbed)

@bot.event
async def on_server_join( server ):
  logging.info('Joined server' + str(server.name))
  logging.info('Server ID' + str(server.id))

async def botstats():
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

    dbots_url = 'https://bots.discord.pw/api/bots' + config['botid'] + 'stats'
    dbl_url = 'https://discordbots.org/api/bots' + config['botid'] + 'stats'
    async with session.post(dbl_url, data=payload, headers=dbl_headers) as dbl_resp:
      logging.info('dbl: posted with code' + print(await dbl_resp.status()))
    async with session.post(dbots_url, data=payload, headers=headers) as resp:
      logging.info('dbots: posted with code' + print(await resp.status()))
    await asyncio.sleep(60 * 60) # report to DBL/dbots every hour

try:
  @bot.event
  async def on_ready():
    logging.info('lolbot - ready')
    loop = asyncio.get_event_loop()
    serverpoll = loop.create_task(botstats())
    logging.info('Bot post loop initalized')
    await bot.change_presence(game=discord.Game(name='with APIs. | ^help | v2.0'))
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

