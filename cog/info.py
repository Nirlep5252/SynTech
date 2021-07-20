from datetime import datetime
import logging
import os

import discord
import psutil
from discord.ext import commands, tasks

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Info is ready')
        global startdate
        startdate = datetime.now()

    @commands.command(aliases=["botinfo", "stats", "status"])
    async def about(self, ctx):
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embed = discord.Embed(color=0xFF5733)
        embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        embed.add_field(name="Library", value="discord.py", inline=False)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )", inline=False)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]), inline=False)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot=bot))
