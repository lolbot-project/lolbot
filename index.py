# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import sys
import logging
import os
import json
from subprocess import check_output
from other import ownerchecks

logging.basicConfig(level=logging.INFO)
description = '''beep boop :)'''
bot = commands.Bot(command_prefix='^', description=description)
config = json.loads(open('config.json').read())

try:
  @bot.event
  async def on_ready():
    print('lolbot - ready')
    await bot.change_presence(game=discord.Game(name='with APIs. | ^help | v2.0'))
except ImportError:
  logging.warn('Module(s) could not be found/not installed')
  logging.warn('Installing automatically')
  check_output(['pip', 'install', '-r', 'requirements.txt'])
  sys.exit('Please relaunch lolbot')
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
async def suggest(self, ctx, *, suggestion: str):
  """Got suggestions?"""    
  person = ctx.message.author.id
  await bot.say('Feedback has been forwarded on to the mailbox.')
  await bot.say(config['sugchannel'], 'Suggestion submitted: `' + str(suggestion) + '`' + str(person))
  
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
@ownerchecks.is_owner()
async def reboot():
  """Duh. Owner only"""
  await bot.say('Second please.')
  logging.info('Restart requested')
  await bot.change_presence(game=discord.Game(name='Restarting'))
  check_output(['sh', 'bot.sh'])
  bot.logout()

@bot.command()
@ownerchecks.is_owner()
async def game(*, game: str):
  """Changes playing status"""
  await bot.change_presence(game=discord.Game(name=game + ' | ^help | v2.0'))

@bot.command()
async def lmgnapi(*, apiarea: str):
  """api.thelmgn.com wrapper"""
  lmgn = requests.get('http://api.thelmgn.com/' + apiarea)
  await bot.say(lmgn.text)

@bot.command()
async def shibe():
  with aiohttp.ClientSession() as shibe:
    """Random shibes, powered by shibe.online"""
    async with shibe.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true') as shibeGet:
      if shibeGet.status == 200:
        shibeJson = shibeGet.json()
        shibeEmbed = discord.Embed(name='lolbot', description='Here is your shibe.', colour=0x6906E8)
        shibeEmbed.set_author(name='lolbot', icon_url=bot.user.default_avatar_url)
        shibeEmbed.set_image(url=shibeJson[0])
        await bot.say(embed=shibeEmbed)

@bot.event
async def on_server_join( server ):
  logging.info('Joined server' + str(server.name))
  logging.info('Server ID' + str(server.id))

try:
  bot.run(config['token'])
except FileNotFoundError:
  logging.error('I can not find config.json!')
  logging.error('Are you sure you are in the same folder as it?')

