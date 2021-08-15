import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.database import db

from config import PREFIXES

from config import Config as config

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.AutoShardedBot(owner_ids = [321750582912221184, 733536002563637298], command_prefix=PREFIXES, intents=intents, case_insensitive=True)
logging.basicConfig(level=logging.INFO) #filename="logs.txt")
bot.load_extension('jishaku')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    logging.info(' __________________________________________________ ')
    logging.info('|                                                  |')
    logging.info('|                 Bot has Started                  |')
    logging.info('+__________________________________________________+')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"!help"))

@bot.event
async def on_message(message):
    e = db.collection.find_one({"user": message.author.id})

    if e is None:
       await bot.process_commands(message)

    else:
       return

load_dotenv('.env')
bot.run(os.getenv('DISCORD_BOT_SECRET'))