from discord.ext.commands import Context
from discord import Forbidden

class LolbotContext(Context):
    async def ok(self):
        try:
            await self.message.add_reaction(self.bot.emoji.success)
        except Forbidden:
            await self.message.channel.send(str(self.bot.emoji.success))
    
    async def not_ok(self):
        try:
            await self.message.add_reaction(self.bot.emoji.fail)
        except Forbidden:
            await self.message.channel.send(str(self.bot.emoji.fail))