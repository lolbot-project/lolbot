import discord
import json
from discord.ext import commands
import utils.errors

class Animemes:
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))
        self.header = {
                'User-Agent': 'lolbot (discord.py/aiohttp)'
        }

    @commands.command()
    async def neko(self, ctx):
        """Shows a random neko picture"""
        async with self.bot.session.get('https://nekos.life/api/neko', headers=self.header) as neko:
            if neko.status == 200:
                img = await neko.json()
                nekoEm = discord.Embed(colour=0x690E8)
                nekoEm.set_image(url=img['neko'])
                await ctx.send(embed=nekoEm)
            else:
                raise utils.errors.ServiceError(f'dude rip (http {neko.status})')

    @commands.command()
    async def lneko(self, ctx):
        """Shows a random lewd neko pic"""
        if ctx.channel.is_nsfw():
            async with self.bot.session.get('https://nekos.life/api/lewd/neko', headers=self.header) as lneko:
                if lneko.status == 200:
                    img = await lneko.json()
                    lnekoEm = discord.Embed(colour=0x690E8)
                    lnekoEm.set_image(url=img['neko'])
                    await ctx.send(embed=lnekoEm)
                else:
                    raise utils.errors.ServiceError(f'dude rip (http {lneko.status})')
        else:
            raise utils.errors.NSFWException('you really think you can do this'
                                             'in a non nsfw channel? lol')

def setup(bot):
    bot.add_cog(Animemes(bot))
