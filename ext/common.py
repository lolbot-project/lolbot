"""
data that's used a ton will be stored here
"""

from core.version import get_version

user_agent = f"lolbot/{get_version()} - https://github.com/lolbot-project"


class Dummy:
    pass


def setup(bot):
    bot.user_agent = user_agent
    bot.emoji = Dummy()
