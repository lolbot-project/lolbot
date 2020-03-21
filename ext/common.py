"""
data that's used a ton will be stored here
"""

from utils.version import get_version

class Dummy:
    pass

def setup(bot):
    bot.user_agent = f'lolbot/{get_version()} - https://github.com/lolbot-project'
    bot.emoji = Dummy()