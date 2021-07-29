import logging

import discord
from discord.ext import commands

from config import Config as config, VERIFIED, MAIN_COLOR


class owners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.developers = config.DEVELOPERS

    async def developer_check(ctx):
       return ctx.author.id in config.DEVELOPERS

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("Owners is ready")

    @commands.command()
    @commands.check(developer_check)
    async def verify(self, ctx):
        embed = discord.Embed(title="Verification", description=f"Please hit the {VERIFIED} emoji to be allowed into the server!", color=MAIN_COLOR).set_footer(text="If you do not get the member or verified role please dm a staff", icon_url=self.bot.user.avatar.url)
        message = await ctx.send(embed=embed)
        await message.add_reaction(VERIFIED)

    @commands.command()
    @commands.check(developer_check)
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was loaded')
        await ctx.send(f'Module {extension} was loaded')

    @commands.command()
    @commands.check(developer_check)
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was unloaded')
        await ctx.send(f'Module **{extension}** is unloaded.')

    @commands.command()
    @commands.check(developer_check)
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        logging.info(f'Module {extension} was reloaded')
        await ctx.send(f'Module **{extension}** was reloaded.')

def setup(bot):
    bot.add_cog(owners(bot=bot))