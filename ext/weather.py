from discord.ext import commands
from utils.metaweather import MetaWeather
from utils.embed import get_embed
from utils.conversion import c_to_f


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if bot.config["integrations"]["metaweather"] is True:
            self.api = MetaWeather()
        else:
            bot.log.warning("Weather was disabled by config. Unloading!")
            bot.unload_cog("Weather")

    def get_icon(self, status: str):
        if status == "sn":
            return ":cloud_snow:"
        elif status == "sl" or "h" or "hr" or "lr":
            return ":cloud_rain:"
        elif status == "s":
            return ":white_sun_rain_cloud:"
        elif status == "hc" or "lc":
            return ":cloud:"
        elif status == "t":
            return ":thunder_cloud_rain"
        elif status == "c":
            return ":sunny:"

    @commands.command()
    async def weather(self, ctx, *, location: str):
        try:
            location = await self.api.get_location(location)
            epic = location[0]
        except:
            raise commands.BadArgument
        possible_conflict = True if len(location) > 3 else False
        result = await self.api.get_current(epic['woeid'])
        embed = get_embed()
        embed.title = f'Weather for {epic["title"]}'
        embed.description = (
            f'{self.get_icon(result["weather_state_abbr"])} Currently: **{result["weather_state_name"]}**\n'
            f':thermometer: Currently: **{result["the_temp"]}** °C / **{c_to_f(result["the_temp"]):.2f}** °F'
        )
        embed.set_footer(text="Powered by MetaWeather")

        await ctx.send(
            f":warning: Your search brung up more than 3 locations. This result may be incorrect."
            if possible_conflict
            else "",
            embed=embed,
        )

    @weather.error
    async def weather_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('The API did not return any results. Try other cities that are close?')

def setup(bot):
    bot.add_cog(Weather(bot))
