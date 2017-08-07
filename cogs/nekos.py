import discord
import aiohttp
import json
from discord.ext import commands

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
                url = img['neko']
                nekoEm.set_image(url=url)
                nekoEm.set_footer(f'nekos.life | *For lewd nekos use {self.config["prefix"]}lneko*')
                await ctx.send(embed=nekoEm)
            else:
                lol = await ctx.send('Something weird happened when I tried to fetch your neko.'
                        f'(HTTP code {neko.status})')

    @commands.command()
    async def lneko(self, ctx):
        """Shows a random lewd neko pic"""
        if ctx.channel.is_nsfw():
            async with self.bot.session.get('https://nekos.life/api/lewd/neko', headers=self.header) as lneko:
                if lneko.status == 200:
                    img = await lneko.json()
                    lnekoEm = discord.Embed(colour=0x690E8)
                    lnekoEm.set_image(url=img['neko'])
                    lnekoEm.set_footer(f'nekos.life | *For normal nekos use {self.config["prefix"]}neko*')
                else:
                    await ctx.send('Something weird happened when I tried to fetch your neko.'
                            f'(HTTP code {lneko.status})')
        else:
            await ctx.send('You\'re not in a NSFW channel. Therefore, I cannot post a'
                    'lewd neko to this channel.')

def setup(bot):
    bot.add_cog(Animemes(bot))
