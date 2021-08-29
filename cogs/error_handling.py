import logging
from utils.exceptions import ItemNotFound, NoItem, NoMoney
import discord
from config import ERROR_COLOR, ERROR_CHANNEL, MONEY_EMOJI

from discord.ext import commands
from discord.ext.commands import MissingPermissions, CheckFailure, CommandNotFound, MissingRequiredArgument, BadArgument


class ErrorHandling(commands.Cog, name="on command error"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            day = round(error.retry_after / 86400)
            hour = round(error.retry_after / 3600)
            minute = round(error.retry_after / 60)
            if day > 0:
                await ctx.send('This command has a cooldown, be sure to wait for ' + str(day) + " day(s)")
            elif hour > 0:
                await ctx.send('This command has a cooldown, be sure to wait for ' + str(hour) + " hour(s)")
            elif minute > 0:
                await ctx.send('This command has a cooldown, be sure to wait for ' + str(minute) + " minute(s)")
            else:
                await ctx.send(f'This command has a cooldown, be sure to wait for {error.retry_after:.2f} second(s)')
        elif isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingPermissions):
            embed = discord.Embed(title="ERROR!", description=f"{error}", color=ERROR_COLOR)
            await ctx.send(embed=embed)
        elif isinstance(error, MissingRequiredArgument):
            embed = discord.Embed(title="ERROR!", description=f"{error}", color=ERROR_COLOR)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="Developer Only", description="You must be a developer to run this command", color=ERROR_COLOR)
            await ctx.send(embed=embed, delete_after=5)
        elif isinstance(error, ItemNotFound):
            embed = discord.Embed(
                title="Item doesn't exist!",
                description=f"The item `{error.item}` does not exist!\nUse `{ctx.clean_prefix}shop` for a list of all items.",
                color=ERROR_COLOR
            )
            await ctx.reply(embed=embed)
        elif isinstance(error, NoItem):
            return await ctx.reply(f"You need a `{error.item}` for this!")
        elif isinstance(error, NoMoney):
            embed = discord.Embed(
                title="You don't have enough money!",
                description=f"You have `{MONEY_EMOJI} {error.current}` but you need `{error.required}$` for this!",
                color=ERROR_COLOR
            )
            await ctx.reply(embed=embed)
        elif isinstance(error, CheckFailure):
            return
        elif isinstance(error, BadArgument):
            embed = discord.Embed(title="ERROR!", description=f"{error}", color=ERROR_COLOR)
            await ctx.send(embed=embed)
        else:
            channel = self.bot.get_channel(ERROR_CHANNEL)
            embed = discord.Embed(title="Error!", description=f"Error:\n```{error}```\nServer:\n```{ctx.guild.name}```\nCommand:\n```{ctx.message.content}```", color=ERROR_COLOR)
            await channel.send(embed=embed)
            logging.info(error)


def setup(bot):
    bot.add_cog(ErrorHandling(bot=bot))
