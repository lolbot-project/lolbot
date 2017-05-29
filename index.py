"""
lolbot - by S Stewart
Under MIT License
Copyright (c) S Stewart 2017

I am looking for developers.
Make a PR if you can help.

Hall of fame:
- Discord API - #python_discord-py
- Discord Bots - #development
and lastly, the Discord.py docs.
I wouldn't be here without them.
"""
# -*- coding: utf-8 -*-
import logging
logging.basicConfig(format='[%(levelname)s] - %(message)s', level=logging.INFO)
from subprocess import check_output
try:
  import discord
  from discord.ext import commands
except ImportError:
  logging.warn('Module(s) could not be found/not installed')
  logging.warn('Installing automatically')
  check_output(['pip', 'install', '-r', 'requirements.txt'])
  sys.exit('Please relaunch lolbot')
else:
  logging.info('Found library, continuing')
import asyncio
import sys
import aiohttp
import json
import time
import datetime
from random import choice as rchoice
try:
  config = json.loads(open('config.json').read())
except FileNotFoundError:
  logging.debug('Can\'t open config to start bot..')
  sys.exit('Fatal error')
except IOError:
  logging.debug('Can\'t open config to start bot..')
  sys.exit('Fatal error')
description = '''beep boop :)'''
bot = commands.AutoShardedBot(command_prefix='^', description=description)
startepoch = int(time.time())

session = aiohttp.ClientSession()

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
@commands.is_owner()
async def evalboi(ctx, *, code: str):
  """Because everyone needs a good eval once in a while."""
  try:
    result = eval(code)
  except Exception as e:
    result = eval(code)
    evalError = discord.Embed(title='Error', description='You made non-working code, congrats you fucker.\n**Error:**\n```' + str(result) + ' ```', colour=0x690E8)
    await ctx.send(embed=evalError)
  else:
    evalDone = discord.Embed(title='Eval', description='Okay, I evaluated that for you.\n**Results:**\n```' + str(result) + '```', colour=0x690E8)
    await ctx.send(embed=evalDone)

@bot.command(hidden=True)
@commands.is_owner()
async def reboot(ctx):
  """Duh. Owner only"""
  rebootPend = discord.Embed(title='Rebooting', description='Rebooting...', colour=0x690E8)
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
async def game(*, game: str):
  """Changes playing status"""
  await bot.change_presence(game=discord.Game(name=game + ' | ^help | v3.0'))

@bot.command()
async def shibe(ctx):
  """Random shibes, powered by shibe.online"""
  async with session.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true') as shibeGet:
      if shibeGet.status == 200:
        shibeJson = await shibeGet.json()
        shibeEmbed = discord.Embed(name='shibe.online', colour=0x690E8)
        shibeEmbed.set_image(url=shibeJson[0])
        await ctx.send(embed=shibeEmbed)

@bot.command()
async def uptime(ctx):
  """Shows uptime of lolbot"""
  upEm = discord.Embed(title='Uptime', colour=0x690E8)
  startedOn = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(startepoch))
  #timeUp = get_up()
  upEm.add_field(name='Started on', value=startedOn)
  #upEm.add_field(name='Uptime', value=timeUp)
  try:
    await ctx.send(embed=upEm)
  except:
    await ctx.send('Could not send due to a error. Tell lold to fix it pls')

@bot.command()
async def stats(ctx):
  """A few stats."""
  # get_owner = bot.get_user_info(config['ownerid'])
  statInfo = await ctx.bot.application_info()
  statEmbed = discord.Embed(title='lolbot stats', description='This bot is powered by [lolbot](https://github.com/xshotD/lolbot),'
  ' a fast and powerful Python bot.', colour=0x690E8)
  statEmbed.add_field(name='Owner', value=statInfo.owner.mention)
  statEmbed.add_field(name='Python', value=sys.version)
  statEmbed.add_field(name='Servers', value=len(bot.guilds))
  statPool = ['What have you done now?', 'Why should I do this again?', 'Oh..',
  'Where did the RAM go?', 'grumble grumble', 'Please hold.', 'No, just, no.',
  'Have you tried rebooting?', 'memework makes the dreamwork!']
  statEmbed.set_footer(text=rchoice(statPool))
  try:
    await ctx.send(embed=statEmbed)
  except:
    await ctx.send('Sorry, I can\'t send the Embed.')
    await ctx.send('Maybe I don\'t have Embed Links permission?')
  else:
    pass

@bot.command(name='8ball')
async def an8ball(ctx, *, question: str):
  pool = ['It is certain', 'Outlook good', 'You may rely on it', 'Ask again later', 'Concentrate and ask again',
  'Reply hazy, try again', 'My reply is no', 'My sources say no']
  ans = rchoice(pool)
  emb = discord.Embed(title='The Magic 8-ball', description='**Question: ' +
   str(question) + '**\nAnswer: ' + str(ans), colour=0x690E8)
  await ctx.send(embed=emb)

@bot.event
async def on_guild_join( guild ):
  logging.info('Joined guild ' + str(guild.name) + 'ID: ' + str(guild.id))
  await botstats()

@bot.event
async def on_guild_remove( guild ):
  logging.info('Left ' + str(guild.name))
  await bot.stats()

# danny code frankenstein :P
async def botstats():
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

"""Stolen from Red which was stolen from R. Danny
Currently not working so commented out
def get_up(self, *, brief=False):
  now = datetime.datetime.utcnow()
  delta = now - self.bot.uptime
  hours, remainder = divmod(int(delta.total_seconds()), 3600)
  minutes, seconds = divmod(remainder, 60)
  days, hours = divmod(hours, 24)

  if not brief:
    if days:
      fmt = '{d} days, {h} hours, {m} minutes, and {s} seconds'
    else:
      fmt = '{h} hours, {m} minutes, and {s} seconds'
    else:
      fmt = '{h}h {m}m {s}s'
    if days:
      fmt = '{d}d ' + fmt

  return fmt.format(d=days, h=hours, m=minutes, s=seconds)
"""
@bot.event
async def on_ready():
  logging.info('lolbot - ready')
  await bot.change_presence(game=discord.Game(name='with APIs. | ^help | v3.0'))
  logging.info('Playing status changed')


bot.run(config['token'])


