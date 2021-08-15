import logging

import discord
from discord.ext import commands

from config import VERIFIED, MAIN_COLOR
from utils.button import Verify, Ticket, Close
from utils.database import db


class owners(commands.Cog, description="No go away developers only"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
            self.bot.add_view(Verify())
            self.bot.add_view(Ticket())
            self.bot.add_view(Close())
            logging.info("Owners is ready")

    @commands.command()
    @commands.is_owner()
    async def verify(self, ctx):
        embed = discord.Embed(title="Verification", description=f"Please hit the button with the {VERIFIED} emoji to be allowed into the server!", color=MAIN_COLOR).set_footer(text="If you do not get the member or verified role please dm a staff", icon_url=self.bot.user.avatar.url)
        message = await ctx.send(embed=embed, view=Verify())
        #await message.add_reaction(VERIFIED)

    @commands.command()
    @commands.is_owner()
    async def ticket(self,ctx):
        embed = discord.Embed(title="Support", description="Please only make a ticket if you need support or have something to ask", color=MAIN_COLOR).set_footer(text="If you have any problems making a ticket please dm a staff", icon_url=self.bot.user.avatar.url)
        await ctx.send(embed=embed, view=Ticket())

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was loaded')
        await ctx.send(f'Module {extension} was loaded')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was unloaded')
        await ctx.send(f'Module **{extension}** is unloaded.')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was reloaded')
        await ctx.send(f'Module **{extension}** was reloaded.')

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def blacklist(self, ctx):
        embed = discord.Embed(title="Blacklist Help", description="!blacklist add {user}\n!blacklist remove {user}", color=MAIN_COLOR)
        await ctx.send(embed=embed)

    @blacklist.command()
    @commands.is_owner()
    async def add(self, ctx, member: discord.Member):
        e = db.collection.find_one({"user": member.id})
        
        if e is None:
                blacklist = {"user": member.id}
                db.collection.insert_one(blacklist)
                await ctx.send(f"You have blacklisted {member.name}")

        else:
            await ctx.send(f"{member.name} is already blacklisted")

    @blacklist.command()
    @commands.is_owner()
    async def remove(self, ctx, member: discord.Member):
        e = db.collection.find_one({"user": member.id})
        
        if e is None:
            await ctx.send(f"{member.name} is not blacklisted")

        else:
            a = db.collection.find_one({"user": member.id})
            db.collection.delete_one(a)
            await ctx.send(f'{member.name} Has been unblacklisted')

def setup(bot):
    bot.add_cog(owners(bot=bot))