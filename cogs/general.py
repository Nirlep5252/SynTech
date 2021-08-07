import asyncio
import datetime
import logging
from functools import partial

import discord
from discord.ext import commands

from config import ERROR_COLOR, MAIN_COLOR, VERIFIED, FUN_COLOR
import random

class general(commands.Cog, description="This well be where all fun commands are"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('General is ready')

    @commands.command()
    async def remindme(self, ctx, time, *, reminder):
        embed = discord.Embed(color=ERROR_COLOR)
        embed.set_footer(
            text="usage !remindme <time> <reminder>",
            icon_url=f"{self.bot.user.avatar.url}")
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning',
                            value='Please specify what do you want me to remind you about.')
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"
        if seconds == 0:
            embed.add_field(name='Warning',
                            value='Please specify a proper duration')
        elif seconds < 300:
            embed.add_field(name='Warning',
                            value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
        elif seconds > 7776000:
            embed.add_field(name='Warning',
                            value='You have specified a too long duration!\nMaximum duration is 90 days.')
        else:
            await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
            await asyncio.sleep(seconds)
            await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
            return
        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question):
     responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
     response = random.choice(responses)
     embed = discord.Embed(title="8ball", description=f"Question: {question}\nAnswer: {response}", color=FUN_COLOR)
     await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(general(bot=bot))