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
import discord
from discord.ext import commands
from osuapi import OsuApi, AHConnector
import osuapi.enums
import utils.errors
import logging


class Osu:
    def __init__(self, bot):
        self.bot = bot
        if bot.config['osu']:
            self.api = OsuApi(bot.config['osu'], connector=AHConnector())
        else:
            self.api = None

    @classmethod
    def osu_mode_converter(self, mode=None):
        if mode is 0 or 'standard' or 'osu!standard' or 'osu!' or None:
            return osuapi.enums.OsuMode.osu
        elif mode is 1 or 'ctb' or 'catchthebeat' or 'osu!catch' or 'catch':
            return osuapi.enums.OsuMode.catch
        elif mode is 2 or 'taiko' or 'osu!taiko':
            return osuapi.enums.OsuMode.taiko
        elif mode is 3 or 'mania' or 'osu!mania':
            return osuapi.enums.OsuMode.mania
        else:
            return 'Unknown'

    def __unload(self):
        logging.info('osu[api]: Closing session.')
        try:
            self.api.close()
        except Exception:
            logging.warning('osu[api]: early close??')
        else:
            logging.info('osu[unload]: OK')

    @commands.command()
    async def osu(self, ctx, u, mode=0):
        """Look up osu! users.
        If the player has spaces in their name, use quotations.
        `^osu "Player Name"`
        If you want different modes, you can use alternative syntax:
        `^osu Cookiezi` (normal)
        `^osu ExGon ctb` (Catch the Beat)
        `^osu n1doking taiko` (Taiko)
        `^osu jakads mania` (Mania)
        Special thanks to khazhyk for the osuapi library.
        """
        if self.api:
            mode = self.osu_mode_converter(mode=mode)
            if mode == 'Unknown':
                raise utils.errors.ServiceError('Unknown mode')
            user = await self.api.get_user(u, mode=mode)
            try:
                user = user[0]
                pp = user.pp_raw  # CHAR SAVING.
                ss = user.count_rank_ss
                s = user.count_rank_s
                a = user.count_rank_a
            except IndexError:
                return await ctx.send('User does not exist, '
                                      'maybe try one that does')
        else:
            raise utils.errors.ServiceError('osu! api key not configured')
        osu_embed = discord.Embed(title=f'osu! stats', colour=0x690E8)
        osu_embed.set_author(name=f'{u} ({user.country}'
                                  f' #{user.pp_country_rank}, global'
                                  f' #{user.pp_rank})',
                             icon_url='https://osu.ppy.sh/images/flags/'
                                      f'{user.country}.png')
        osu_embed.set_thumbnail(url=f'https://a.ppy.sh/{user.user_id}')
        osu_embed.add_field(name='Hits (300/100/50)', value=f'{user.count300}/'
                                                            f'{user.count100}/'
                                                            f'{user.count50}')
        osu_embed.add_field(name='Play count', value=user.playcount)
        osu_embed.add_field(name='Ranked score', value=user.ranked_score)
        osu_embed.add_field(name='Total score', value=user.total_score)
        osu_embed.add_field(name='Level', value=int(user.level))
        osu_embed.add_field(name='Total PP', value=f'{round(pp, 2)} PP')
        osu_embed.add_field(name='Accuracy', value=f'{user.accuracy:.1f}%')
        osu_embed.add_field(name='Plays (SS/S/A)', value=f'{ss}/{s}/{a}')
        await ctx.send(embed=osu_embed)


def setup(bot):
    bot.add_cog(Osu(bot))
