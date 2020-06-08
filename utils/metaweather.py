from aiohttp import ClientSession
from urllib.parse import quote_plus


class MetaWeather:
    def __init__(self):
        self.http = ClientSession()
        self.base_url = "https://www.metaweather.com/api/"

    async def get_location(self, location: str):
        location = quote_plus(location)
        yes = await self.http.get(f"{self.base_url}location/search?query={location}")
        yes = await yes.json()
        return yes

    async def get_current(self, location: int):
        async with self.http.get(f"{self.base_url}location/{location}") as yes:
            yes = await yes.json()
            # I'm sorry god
            yes = yes["consolidated_weather"]
            yes = yes[0]
            return yes
