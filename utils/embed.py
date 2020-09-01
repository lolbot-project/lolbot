from discord import Embed as thonk

class Embed(thonk):
    def __init__(self, *args, **kwargs):
        """
        Helper for discord.Embed.

        :returns: discord.Embed
        """
        self.colour = 0x690E8

def get_embed():
    """
    Helper for discord.Embed.
    
    :returns: discord.Embed
    """
    return Embed()
