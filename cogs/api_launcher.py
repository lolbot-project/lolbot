from quart.serving import Server
from quart.logging import create_serving_logger
from cogs.api import app
from discord.ext import commands

class WebAPILauncher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loop = bot.loop
        app.bot = bot
        bot.api_instance = app
        self.start_app()

    def start_app(self):
        self.bot.api_task = self.loop.create_task(self.loop.create_server(
            lambda: Server(app, self.bot.loop, create_serving_logger(
            ), '%(h)s %(r)s %(s)s %(b)s %(D)s', keep_alive_timeout=5),
            host='127.0.0.1', port=6142, ssl=None
        ))


def __unload(bot):
    bot.api_task.cancel()


def setup(bot):
    bot.add_cog(WebAPILauncher(bot))
