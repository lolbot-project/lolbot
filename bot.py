"""
lolbot rewrite - (c) 2020 tilda under MIT License

This module contains code needed to start the bot, including other services,
such as the API
"""

from discord.ext import commands
from logbook import Logger, StreamHandler, INFO
from logbook.compat import redirect_logging
from sys import stdout
from utils.config import Config
import os
import asyncio
from core.bot import Lolbot
from rich import traceback

redirect_logging()
traceback.install()
StreamHandler(stdout, level=INFO).push_application()
log = Logger("lolbot")

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ModuleNotFoundError:
    log.warning("Ignoring uvloop due to being on win32")
except Exception:
    log.warning("unable to setup uvloop", exc_info=True)

config = Config("config.yaml").config
help_command = commands.help.DefaultHelpCommand(dm_help=None)
bot = Lolbot(
    command_prefix=commands.when_mentioned_or(config["bot"]["prefix"]),
    description="hi im a bot",
    help_command=help_command,
    logger=log,
)

if __name__ == "__main__":
    for ext in os.listdir("ext"):
        if ext.endswith(".py"):
            try:
                log.info(f"attempting to load {ext}")
                ext = ext.replace(".py", "")
                bot.load_extension(f"ext.{ext}")
            except Exception:
                log.error(f"failed to load {ext}", exc_info=True)
            else:
                log.info(f"successfully loaded {ext}")
    log.info("loading jishaku")
    bot.load_extension("jishaku")

bot.run(config["tokens"]["discord"])
