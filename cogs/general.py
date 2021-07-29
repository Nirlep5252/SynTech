import asyncio
import datetime
import logging

import discord
from discord.ext import commands

from config import ERROR_COLOR, MAIN_COLOR, VERIFIED
from utils.button import Button
from utils.select import Select

class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('General is ready')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id != 870172390108327936:
            return
        guild = self.bot.get_guild(payload.guild_id)
        role = guild.get_role(870159097524273262)
        member_role = guild.get_role(870161379141763092)
        if str(payload.emoji) == VERIFIED:
            await payload.member.add_roles(role)
            await payload.member.add_roles(member_role)
            embed = discord.Embed(title="Verified", description=f"You have been Verified, You can now chat with the other developers!", color=MAIN_COLOR).set_footer(text=f"Welcome to the server", icon_url=self.bot.user.avatar.url)
            await payload.member.send(embed=embed)

    @commands.command()
    async def hi(self, ctx):
       await ctx.send("Hi", view=Select())

    @commands.command()
    async def button(self, ctx):
        await ctx.send("Do it", view=Button())

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

def setup(bot):
    bot.add_cog(general(bot=bot))