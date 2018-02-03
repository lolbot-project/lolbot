# etc data
version = '2.0'
user_agent = {
    'User-Agent': 'lolbot/{} - https://lolbot.lmao.tf'.format(version)
}

# Dummy class, holds data
# This forms a "object"
# When used, you can now
# hold data inside the variable
# you attached the class to.
# Magic!
class Dummy:
    pass

def setup(bot):
    # Setup a bot emote register, to store emojis for use
    # e.g. notcheck
    bot.emoji = Dummy()
