import logging
import discord
from discord.ext import commands

class general(commands.Cog):
    def __init__(self, bot):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Info is ready')


def setup(bot):
    bot.add_cog(general(bot=bot))
