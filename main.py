import logging
import os
import time

import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True, presences=True)
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)
logging.basicConfig(level=logging.INFO)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_ready():
    logging.info('Bot is ready')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name=f"Add text here"))

@bot.command(name="ping", usage="", description="Display the bot's ping.")
@commands.cooldown(1, 2, commands.BucketType.member)
async def ping(ctx):
    before = time.monotonic()
    embed = discord.Embed(title="Ping!", description=f'Ping')
    message = await ctx.send(embed=embed)
    ping = (time.monotonic() - before) * 1000
    embed2 = discord.Embed(title="Pong!", description=f'Api Ping  !  `{round(bot.latency * 1000)}` ms\nBot Ping ! `{int(ping)}` ms')
    await message.edit(embed=embed2)

load_dotenv('.env')
bot.run(os.getenv('DISCORD_BOT_SECRET'))
