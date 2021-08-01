import asyncio
import datetime
import logging

import discord
from discord.ext import commands

from config import ERROR_COLOR, MAIN_COLOR, VERIFIED
from utils.database import db


class ticket_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Tickets is ready')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def close(self, ctx):

        e = db.collection.find_one(
            {"ticket_guild_id": ctx.guild.id, "ticket": int(ctx.channel.topic)})

        if e is None:
            await ctx.send("User has no ticket")

        elif not ctx.channel.topic:
            ctx.send("No")
            return

        else:
            a = db.collection.find_one({"ticket_guild_id": ctx.guild.id, "ticket": int(ctx.channel.topic)})
            db.collection.delete_one(a)
            embed = discord.Embed(title="Closed", description=f"We hope we fixed your problem!", color=MAIN_COLOR).set_footer(text="If you think this was a mistake dm a staff", icon_url=self.bot.user.avatar.url)
            user = self.bot.get_user(int(ctx.channel.topic))
            await user.send(embed=embed)
            await ctx.channel.delete()

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def add(self, ctx, member: discord.Member):
        e = db.collection.find_one(
            {"ticket_guild_id": ctx.guild.id, "ticket": int(ctx.channel.topic)})

        if e is None:
            await ctx.send("this is no ticket")

        else:
            await ctx.channel.set_permissions(member, send_messages=True, view_channel=True)
            await ctx.send(f"I have added {member.name}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def remove(self, ctx, member: discord.Member):
        e = db.collection.find_one(
            {"ticket_guild_id": ctx.guild.id, "ticket": int(ctx.channel.topic)})

        if e is None:
            await ctx.send("this is no ticket")

        else:
            await ctx.channel.set_permissions(member, send_messages=False, view_channel=False)
            await ctx.send(f"I have removed {member.name}")

    @add.error
    async def add_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.ConversionError):
            message = str(error)
        else:
            message = "This is not a ticket channel"

        await ctx.send(message)

    @remove.error
    async def remove_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.ConversionError):
            message = str(error)
        else:
            message = "This is not a ticket channel"

        await ctx.send(message)

    @close.error
    async def close_error(self, ctx: commands.Context, error: commands.CommandError):

        if isinstance(error, commands.ConversionError):
            message = str(error)
        else:
            message = "This is not a ticket channel"

        await ctx.send(message)

def setup(bot):
    bot.add_cog(ticket_cog(bot=bot))