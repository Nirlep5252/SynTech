import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import Config as config

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
logging.basicConfig(level=logging.INFO)
bot.load_extension('jishaku')

async def developer_check(ctx):
    return ctx.author.id in config.DEVELOPERS

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    logging.info('Bot is ready')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"WIP"))

load_dotenv('.env')
bot.run(os.getenv('DISCORD_BOT_SECRET'))
