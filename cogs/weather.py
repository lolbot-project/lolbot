"""
The MIT License (MIT)

Copyright (c) 2018 tilda

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
# thanks luna haha
# noinspection PyPackageRequirements
from discord.ext import commands
# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
import utils.errors as uerrs
import pyowm

W_CLEAR_SKY = ':sunny:'
W_FEW_CLOUDS = ':white_sun_small_cloud:'
W_SCATTERED_CLOUDS = ':partly_sunny:'
W_BROKEN_CLOUDS = ':cloud:'
W_SHOWER_RAIN = ':cloud_rain:'
W_RAIN = ':cloud_rain:'
W_THUNDERSTORM = ':thunder_cloud_rain:'
W_SNOW = ':snowflake:'
W_MIST = ':foggy:'

OWM_ICONS = {
    '01n': W_CLEAR_SKY,
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
        self.loop = self.bot.loop
        self.config = self.bot.config
        if self.config['owm']:
            self.owm = pyowm.OWM(self.config['owm'])
        else:
            self.owm = None

    @commands.command()
    @commands.cooldown(2, 5)
    async def weather(self, ctx, *, loc: str):
        """Grabs the weather from OpenWeatherMap"""
        if self.owm:
            try:
                future = self.loop.run_in_executor(None,
                                                   self.owm.weather_at_place,
                                                   loc)
                observation = await future

            except pyowm.exceptions.not_found_error.NotFoundError:
                return await ctx.send('Location not found, maybe be more specific')
            except Exception as e:
                raise uerrs.ServiceError(e)
            w = observation.get_weather()
            _wg = lambda t: w.get_temperature(t)['temp']
            _icon = w.get_weather_icon_name()
            icon = OWM_ICONS.get(_icon, '*<no icon>*')
            status = w.get_detailed_status()
            location = observation.get_location()
            em = discord.Embed(title=f'Weather for {location.get_name()}',
                               colour=0x690E8)
            em.add_field(name='Situation', value=f'{status} {icon}')
            em.add_field(name='Temperature', value=f'`{_wg("celsius")} °C, {_wg("fahrenheit")} °F`')
            await ctx.send(embed=em)
        else:
            raise uerrs.ServiceError('OpenWeatherMap API not configured.')


def setup(bot):
    bot.add_cog(Weather(bot))
