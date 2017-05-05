from discord.ext import commands
import json

config = json.loads(open('config.json').read())
def is_owner():
  try:
    return commands.check(lambda ctx: ctx.message.author.id == config['ownerid'])
  except discord.ext.commands.errors.CheckFailure:
    noperms = discord.Embed(name='Error', description='You have no permissions to use this command.')
    return commands.bot.say(embed=noperms)
