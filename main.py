import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.database import db, prefix_collection

from config import PREFIXES, DEVELOPERS


async def get_prefix(bot: commands.AutoShardedBot, message: discord.Message) -> list[str]:
    if not message.guild:
        return PREFIXES

    guild_id = message.guild.id
    document = prefix_collection.find_one({"_id": guild_id})

    if not document:
        return PREFIXES
    return document["prefixes"]

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.AutoShardedBot(
    owner_ids=DEVELOPERS,
    command_prefix=get_prefix,
    intents=intents,
    case_insensitive=True,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True, replied_user=True),
    strip_after_prefix=True
)
logging.basicConfig(level=logging.INFO)
bot.load_extension('jishaku')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


@bot.event
async def on_ready():
    logging.info(' __________________________________________________ ')
    logging.info('|                                                  |')
    logging.info('|                 Bot has Started                  |')
    logging.info('|                                                  |')
    logging.info('+__________________________________________________+')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="!help"))


@bot.event
async def on_message(message):
    e = db.collection.find_one({"user": message.author.id})

    if e is None:
        await bot.process_commands(message)
    else:
        return

load_dotenv('.env')

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_BOT_SECRET'))