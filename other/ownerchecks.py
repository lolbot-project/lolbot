from discord.ext import commands
import json

config = json.loads(open('config.json').read())
def is_owner():
  return commands.check(lambda ctx: ctx.message.author.id == config['ownerid'])
