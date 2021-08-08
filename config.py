import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

Website_link = 'https://github.com/Synterra-Technologies'

#Color config

MAIN_COLOR = discord.Color.green()
ERROR_COLOR = discord.Color.red()
WARN_COLOR = discord.Color.orange()
NSFW_COLOR = discord.Color.purple()
FUN_COLOR = discord.Color.blue()

#Bot config

DEVELOPER = 'Blue.#1270'
VERSION = "1.3"
PREFIXES = ['!']
VERIFIED = '<a:check:870155042659921941>'
TICKET_EMOJI = '🎟️'
CLOSE_EMOJI = '🛑'
LOG_CHANNEL = 869369735886823455
TICKETS_CATEGORY = 871207377750347796
STAFF_ROLE = 870410239806165023

#Global chat config

GLOBAL_CHAT_WEBHOOK = f"{os.getenv('WEBHOOK_1')}"
GLOBAL_CHAT_WEBHOOK_2 = f"{os.getenv('WEBHOOK_2')}"
GLOBAL_CHAT_CHANNEL = 872195315535601745
GLOBAL_CHAT_CHANNEL_2 = 872206748600131644

class Config:
    DEVELOPERS = [733536002563637298, 321750582912221184]