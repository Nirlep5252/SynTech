import logging

from discord.ext import commands

from config import Config as config

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