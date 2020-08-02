from discord.ext import commands
from utils.openweathermap import OpenWeatherMap
from utils.embed import get_embed
from utils.errors import WeatherException
from utils.conversion import c_to_f


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if bot.config["integrations"]["openweathermap"] is True:
            self.owm = OpenWeatherMap(bot.config["tokens"]["openweathermap"])
        else:
            bot.log.warning("Weather was disabled by config. Unloading!")
            bot.unload_cog("Weather")

    def get_icon(self, status: str):
        if status == "01d":
            return ":sunny:"
        elif status == "01n":
            return ":new_moon:"
        elif status == "02d" or "02n":
            return ":white_sun_small_cloud:"
        elif status == "03d" or "03n" or "04d" or "04n":
            return ":cloud:"
        elif status == "09d" or "09n":
            return ":cloud_rain:"
        elif status == "10d" or "10n":
            return ":white_sun_rain_cloud:"
        elif status == "11d" or "11n":
            return ":thunder_cloud_rain:"
        elif status == "13d" or "13n":
            return ":cloud_snow:"
        elif status == "50d" or "50n":
            return ":dash:"  # lol twemoji doesnt have anything for this

    @commands.command()
    async def weather(self, ctx, *, location: str):
        try:
            current = await self.owm.get_current(location)
        except WeatherException as e:
            if e.cod == 404:
                return await ctx.send(
                    "City not found, perhaps try another one near it."
                )
            elif e.cod == 429:
                return await ctx.send(
                    "Too many people are currently trying to use this command. Try again in a bit?"
                )
        embed = get_embed()
        embed.title = f'Weather for {current["city"]}'
        embed.description = (
            f'{self.get_icon(current["icon"])} Currently: **{current["description"]}**\n'
            f':thermometer: Temperature: **{current["temp_c"]}** °C / **{current["temp_f"]}** °F'
        )
        embed.set_footer(text="Powered by OpenWeatherMap")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Weather(bot))
