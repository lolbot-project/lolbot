import discord
from discord.ext import commands
from osuapi import OsuApi, AHConnector
import osuapi.enums
import utils.errors

class Osu:
    def __init__(self, bot):
        self.bot = bot
        if bot.config['osu']:
            self.api = OsuApi(bot.config['osu'], connector=AHConnector())
        else:
            self.api = None

    def osu_mode_converter(self, mode=None):
        if mode is 'standard' or 'osu!standard' or None:
            return osuapi.enums.OsuMode.osu
        elif mode is 'ctb' or 'catchthebeat' or 'osu!catch' or 'catch':
            return osuapi.enums.OsuMode.catch
        elif mode is 'taiko' or 'osu!taiko':
            return osuapi.enums.OsuMode.taiko
        elif mode is 'mania' or 'osu!mania':
            return osuapi.enums.OsuMode.mania

    @commands.group()
    async def osu(self, ctx):
        """Commands for osu!"""
        if ctx.invoked_subcommand is None or 'help':
            help_em = discord.Embed(title='Commands for osu!', colour=0x690E8)
            await ctx.send(embed=help_em)
                    
    @osu.group()
    async def user(self, ctx, u: str, mode: osu_mode_converter):
        """Returns information on a osu! player.
        If the player name you are searching has spaces, use quotation marks.
        e.g. ^osu "player name with spaces"
        Special thanks to khazhyk for the library this command uses.

        By default this command defaults to osu!standard.
        """
        if self.api:
            user = await self.api.get_user(u, mode=mode)
        else:
            raise utils.errors.ServiceError('osu! api key not configured')
        osu_embed = discord.Embed(title=f'osu! stats for {u}', colour=0x690E8)
        osu_embed.add_field(name='Country', value=user.country)
        osu_embed.add_field(name='User ID', value=user.user_id)
        osu_embed.add_field(name='Hits (300 score)', value=user.count300)
        osu_embed.add_field(name='Hits (100 score)', value=user.count100)
        osu_embed.add_field(name='Hits (50 score)', value=user.count50)
        osu_embed.add_field(name='Play count', value=user.playcount)
        osu_embed.add_field(name='Ranked score', value=user.ranked_score)
        osu_embed.add_field(name='Total score', value=user.total_score)
        osu_embed.add_field(name='Global rank', value=user.pp_rank)
        osu_embed.add_field(name='Country rank', value=user.pp_country_rank)
        osu_embed.add_field(name='Level', value=user.level)
        osu_embed.add_field(name='Total PP', value=user.pp_raw)
        osu_embed.add_field(name='Accuracy', value=user.accuracy)
        osu_embed.add_field(name='Total SS plays', value=user.count_ss_ranks)
        osu_embed.add_field(name='Total S plays', value=user.count_s_ranks)
        osu_embed.add_field(name='Total A plays', value=user.count_a_ranks)

def setup(bot):
    bot.add_cog(Osu(bot))
