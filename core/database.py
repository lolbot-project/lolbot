from rethinkdb import RethinkDB

class DatabaseConnection:
    def __init__(self, host: str, port: int):
        self.rethink = RethinkDB()
        self.rethink.set_loop_type('asyncio')

    async def connect(self):
        return self.rethink.connect(host=self.host, port=self.port)
