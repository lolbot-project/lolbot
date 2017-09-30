from discord.ext import commands
import utils.errors as uerrs
import pyowm

W_CLEAR_SKY =           ':sunny:'
W_FEW_CLOUDS =          ':white_sun_small_cloud:'
W_SCATTERED_CLOUDS =    ':partly_sunny:'
W_BROKEN_CLOUDS =       ':cloud:'
W_SHOWER_RAIN =         ':cloud_rain:'
W_RAIN =                ':cloud_rain:'
W_THUNDERSTORM =        ':thunder_cloud_rain:'
W_SNOW =                ':snowflake:'
W_MIST =                ':foggy:'

OWM_ICONS = {
    '01d': W_CLEAR_SKY,
    '02d': W_FEW_CLOUDS,
    '03d': W_SCATTERED_CLOUDS,
    '04d': W_BROKEN_CLOUDS,
    '09d': W_SHOWER_RAIN,
    '10d': W_RAIN,
    '11d': W_THUNDERSTORM,
    '13d': W_SNOW,
    '50d': W_MIST,
}

class Weather:
    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config
        if self.config['owm']:
            self.owm = pyowm.OWM(self.config['owm'])
        else:
            self.owm = None

    @commands.command()
    @commands.cooldown(2, 5)
    async def weather(self, ctx, *, loc: str):
        if self.owm:
            try:
                future = self.loop.run_in_executor(None, \
                    self.owm.weather_at_place, location)
                observation = await future
            except Exception as e:
                raise uerrs.ServiceError(e)
                return
            w = observation.get_weather()
            _wg = lambda t: w.get_temperature(t)['temp']
            _icon = w.get_weather_icon_name()
            icon = OWM_ICONS.get(_icon, '*<no icon>*')
            status = w.get_detailed_status()
            em = discord.Embed(title=f"Weather for '{location}'")
            o_location = observation.get_location()
            em.add_field(name='Location', value=f'{o_location.get_name()}')
            em.add_field(name='Situation', value=f'{status} {icon}')
            em.add_field(name='Temperature', value=f'`{_wg("celsius")} °C, {_wg("fahrenheit")} °F`')
            await ctx.send(embed=em)
        else:
            raise uerrs.ServiceError('This instance does not have a OpenWeatherMap API key configured.')
            return

def setup(bot):
    bot.add_cog(Weather(bot))
