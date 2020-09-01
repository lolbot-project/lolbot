from core.config import Config
from ext.common import user_agent
from core.version import get_version
from core.prefix import get_prefix
from hypercorn.asyncio.run import Server
from discord.ext import commands
from api.server import app as webapp
from rethinkdb import RethinkDB
import aiohttp
import hypercorn.config
import discord
import time

# Thanks: https://github.com/slice/dogbot/blob/master/dog/bot.py#L19
async def _boot_hypercorn(app, config, *, loop):
    socket = config.create_sockets()
    server = await loop.create_server(
        lambda: Server(app, loop, config), host="127.0.0.1", port=app.bot.config["api"]["port"] 
    )
    return server

class Dummy:
    pass

class Lolbot(commands.AutoShardedBot):
    def __init__(self, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logger
        self.config = Config("config.yaml").config
        self.session = self.loop.create_task(self._create_http_session()).result()

        self.beta = 'b' if not self.config["bot"]["production"] else ''
        self.version = get_version()
        self.prefix = get_prefix(self.config)

        self.rethink = RethinkDB()
        self.rethink.set_loop_type("asyncio")
        self.db_conn = None

        if self.loop.is_running():
            self.loop.create_task(self._connect_rethink())
        else:
            self.loop.run_until_complete(self._connect_rethink())

        if self.config["api"]["enabled"]:
            webapp.bot = self
            self.webapp = webapp
            self.http_server = None
            self.http_server_config = hypercorn.Config.from_mapping(self.config["api"])
            self.loop.create_task(self._boot_http_server())
        else:
            self.log.info("api disabled, skipping http server boot")

        self.emoji = Dummy() # lol
        self.emoji.fail = discord.utils.get(self.emojis, name="l_fail")
        self.emoji.success = discord.utils.get(self.emojis, name="l_check")
        self.emoji.load = discord.utils.get(self.emojis, name="l_process")

    async def _create_http_session(self):
        return await aiohttp.ClientSession(loop=self.loop, headers={'User-Agent': user_agent})

    async def _connect_rethink(self):
        """
        Returns a connection for RethinkDB.
        """
        self.db_conn = await self.rethink.connect(self.config["rethink"]["host"], self.config["rethink"]["port"], db='lolbot')

    async def report_error(self, error: Exception, user: int, command: str):
        return await self.rethink.table("errors").insert({
            "exception": str(error),
            "info": {
                "id": user,
                "command": command
            }
        })

    async def on_ready(self):
        self.log.info(f"whats poppin mofos! {self.user!s}")
        await self.change_presence(
            activity=discord.Streaming(
                name=f"{self.prefix}help | v{self.version}{self.beta}",
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
            self.log.info(f"http server running: {self.http_server!r}")
        except Exception:
            self.log.exception("http server creation failed")
