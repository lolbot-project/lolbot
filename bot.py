"""
lolbot rewrite - (c) 2020 tilda under MIT License

This module contains code needed to start the bot, including other services,
such as the API
"""

from discord.ext import commands
import logging
from utils.config import Config
import os
import asyncio
from core.bot import Lolbot
from rich import traceback

traceback.install()

logging.basicConfig(
    format="(%(asctime)s) [%(levelname)s] - %(message)s", level=logging.INFO
)

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ModuleNotFoundError:
    logging.warning("Ignoring uvloop due to being on win32")
except Exception:
    logging.warning("unable to setup uvloop", exc_info=True)

config = Config("config.yaml").config
help_command = commands.help.DefaultHelpCommand(dm_help=None)
bot = Lolbot(
    command_prefix=commands.when_mentioned_or(config["bot"]["prefix"]),
    description="hi im a bot",
    help_command=help_command,
)

if __name__ == "__main__":
    for blahblah, blahblahblah, exts in os.walk("ext"):
        for ext in exts:
            if ext.endswith(".py"):
                try:
                    logging.info(f"attempting to load {ext}")
                    ext = ext.replace(".py", "")
                    bot.load_extension(f"ext.{ext}")
                except Exception:
                    logging.error(f"failed to load {ext}", exc_info=True)
                else:
                    logging.info(f"successfully loaded {ext}")
    logging.info("loading jishaku")
    bot.load_extension("jishaku")

bot.run(config["tokens"]["discord"])
