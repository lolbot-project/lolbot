import discord
import aiohttp
import json
from discord.ext import commands

class Animemes:
    def __init__(self, bot):
        self.bot = bot
        self.config = json.load(open('config.json'))
        self.base = 'https://nekos.life/api/'
        self.nekos = 'neko'
        self.nlewd = 'lewd/neko'
        self.header = {
                'User-Agent': 'lolbot (discord.py/aiohttp)'
        }

    @commands.command()
    async def neko(self, ctx):
        """Shows a random neko picture"""
        load = await ctx.send('Fetching a neko...')
        async with self.bot.session.get(f'{self.base}{self.nekos}', headers=self.header) as neko:
            load.delete()
            if neko.status == 200:
                img = await neko.json()
                nekoEm = discord.Embed(colour=0x690E8)
                nekoEm.set_image(img['neko'])
                nekoEm.set_footer(f'nekos.life | *For lewd nekos use {self.config["prefix"]}lneko*')
            else:
                lol = await ctx.send('Something weird happened when I tried to fetch your neko.'
                        f'(HTTP code {neko.status})')

    @commands.command()
    async def lneko(self, ctx):
        """Shows a random lewd neko pic"""
        if ctx.channel.is_nsfw():
            load = await ctx.send('Fetching a lewd neko...')
            async with self.bot.session.get(f'{self.base}{self.nlewd}', headers=self.header) as lneko:
                load.delete()
                if lneko.status == 200:
                    img = await lneko.json()
                    lnekoEm = discord.Embed(colour=0x690E8)
                    lnekoEm.set_image(img['neko'])
                    lnekoEm.set_footer(f'nekos.life | *For normal nekos use {self.config["prefix"]}neko*')
                else:
                    await ctx.send('Something weird happened when I tried to fetch your neko.'
                            f'(HTTP code {lneko.status})')
        else:
            await ctx.send('You\'re not in a NSFW channel. Therefore, I cannot post a'
                    'lewd neko to this channel.')

def setup(bot):
    bot.add_cog(Animemes(bot))
