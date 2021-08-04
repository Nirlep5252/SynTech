from datetime import datetime
import time
import logging
import os

import discord
import psutil
from discord.ext import commands, tasks
from config import MAIN_COLOR, GLOBAL_CHAT_WEBHOOK, GLOBAL_CHAT_CHANNEL_2, PREFIXES
from discord import Webhook
import aiohttp

class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Info is ready')

    @commands.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", color=MAIN_COLOR)
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}", inline=False)
        embed.add_field(name="Server Created", value=f"{ctx.guild.created_at.__format__('%A, %d. %B %Y')}", inline=False)
        embed.add_field(name="Verification", value=f"{str(ctx.guild.verification_level).upper()}", inline=False)
        embed.add_field(name="Member Count", value=f"{ctx.guild.member_count} Members", inline=False)
        embed.add_field(name="Highest Role", value=f"{ctx.guild.roles[-2]}", inline=False)
        embed.add_field(name="Categories", value=f"{len(ctx.guild.categories)} Categories", inline=False)
        embed.add_field(name="Text Channels", value=f"{len(ctx.guild.text_channels)} Channels", inline=False)
        if len(ctx.guild.voice_channels) <= 0:
          embed.add_field(name="Voice Channels", value=f"No voice channels :tired_face:")

        elif len(ctx.guild.voice_channels) <= 1:
            embed.add_field(name="Voice Channels", value=f"1 Voice Channel")

        else:
           embed.add_field(name="Voice Channels", value=f"{len(ctx.guild.voice_channels)} Voice Channels")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def ping(self, ctx):
       before = time.monotonic()
       embed = discord.Embed(title="Ping!", description=f'Ping', color=MAIN_COLOR)
       message = await ctx.send(embed=embed)
       ping = (time.monotonic() - before) * 1000
       ping_embed = discord.Embed(title="Pong!", description=f'Api Ping  !  `{round(self.bot.latency * 1000)}` ms\nBot Ping ! `{int(ping)}` ms', color=MAIN_COLOR)
       await message.edit(embed=ping_embed)

    @commands.command(aliases=["botinfo", "stats", "status"])
    async def about(self, ctx):
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = sum(g.member_count for g in self.bot.guilds) / len(self.bot.guilds)

        embed = discord.Embed(color=discord.Color.red())
        embed.set_thumbnail(url=ctx.bot.user.avatar.url)
        embed.add_field(name="Library", value="discord.py", inline=False)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avgmembers:,.2f} users/server )", inline=False)
        embed.add_field(name="Commands loaded", value=len([x.name for x in self.bot.commands]), inline=False)
        embed.add_field(name="RAM", value=f"{ramUsage:.2f} MB", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(info(bot=bot))
