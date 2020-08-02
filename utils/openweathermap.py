from aiohttp import ClientSession
from utils.conversion import c_to_f
from utils.errors import WeatherException

class OpenWeatherMap:
    def __init__(self, api_key: str):
        self.http = ClientSession()
        self.base_url = f'https://api.openweathermap.org/data/2.5/weather?appid={api_key}'
    
    async def get_current(self, location: str):
        async with self.http.get(self.base_url + f'&q={location}&units=metric') as current:
            json = await current.json()
            if current.status != 200:
                raise WeatherException(json)
            return {
                "city": json.get('name'),
                "temp_c": json.get('main').get('temp'),
                "temp_f": round(c_to_f(json.get('main').get('temp')), 2),
                "icon": json.get('weather')[0]['icon'],
                "description": json.get('weather')[0]['description']
            }