import logging

import discord
from discord.ext import commands

from utils.button import Button
from utils.select import Select

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('General is ready')


    @commands.command()
    async def hi(self, ctx):
       await ctx.send("Hi", view=Select())

    @commands.command()
    async def button(self, ctx):
        await ctx.send("Do it", view=Button())

def setup(bot):
    bot.add_cog(general(bot=bot))