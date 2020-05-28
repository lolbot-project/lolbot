from utils.config import Config
from ext.common import user_agent
from utils.version import get_version
from utils.prefix import get_prefix
from hypercorn.asyncio.run import Server
from discord.ext import commands
import aiohttp
import hypercorn.config
import logging
import discord
import time

# Thanks: https://github.com/slice/dogbot/blob/master/dog/bot.py#L19
async def _boot_hypercorn(app, config, *, loop):
    socket = config.create_sockets()
    server = await loop.create_server(
        lambda: Server(app, loop, config), sock=socket.insecure_sockets[0]
    )
    return server

class Lolbot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = Config("config.yaml").config
        self.session = aiohttp.ClientSession(
            loop=self.loop, headers={"User-Agent": user_agent}
        )
        if self.config["api"]["enabled"]:
            webapp.bot = self
            self.webapp = webapp
            self.http_server = None
            self.http_server_config = hypercorn.Config.from_mapping(self.config["api"])
            self.loop.create_task(self._boot_http_server())
        else:
            logging.info("api disabled, skipping http server boot")

    async def on_ready(self):
        logging.info("lolbot has started up")
        await self.change_presence(
            activity=discord.Streaming(
                name=f"{get_prefix(self.config)}help | v{get_version()}",
                url="https://twitch.tv/monstercat",
            )
        )
        self.init_time = time.time()

    async def on_message(self, message):
        if message.author.bot:
            return
        ctx = await self.get_context(message)
        await self.invoke(ctx)

    async def _boot_http_server(self):
        try:
            self.http_server = await _boot_hypercorn(
                self.webapp, self.http_server_config, loop=self.loop
            )
            logging.info("http server running: %r", self.http_server)
        except Exception:
            logging.exception("http server creation failed")
