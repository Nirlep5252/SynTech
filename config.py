import discord
import os

Website_link = 'https://github.com/Synterra-Technologies'

# Color config

MAIN_COLOR = discord.Color.green()
ERROR_COLOR = discord.Color.red()
WARN_COLOR = discord.Color.orange()
NSFW_COLOR = discord.Color.purple()
FUN_COLOR = discord.Color.blue()

# Bot config

DEVELOPER = 'Blue.#1270'
DEVELOPERS = [733536002563637298, 321750582912221184, 558861606063308822]  # adding my id while i was testing with bot :scared: u can remove later
VERSION = "1.3"
PREFIXES = ['!']
BAD_WORDS = ["fuck"]

# Emojis

VERIFIED = '<a:check:870155042659921941>'
TICKET_EMOJI = '🎟️'
CLOSE_EMOJI = '🛑'
MONEY_EMOJI = '<:1money:874004784301096961>'
FORWARD_ARROW = '<:forward:854355986256625664>'
BACK_ARROW = '<:_back:854355985988845610>'

# Channels & Roles

LOG_CHANNEL = 869369735886823455
ERROR_CHANNEL = 874788663651889162
TICKETS_CATEGORY = 871207377750347796
CHAT_BOT_CHANNEL = 878799637568438353
STAFF_ROLE = 870410239806165023
SUGGESTIONS_CHANNEL = 879186766102421576

# Cog stuff

EMOJIS_FOR_COGS = {
    'nsfw': '🔞',
    'images': '📸',
    'moderation': '🛠️',
    'general': '🌍',
    'tickets': '🎟️',
    'info': 'ℹ️',
    'owners': '⛔',
    'money': '<:1money:874004784301096961>'
}

# Global chat config

GLOBAL_CHAT_WEBHOOK = f"{os.getenv('WEBHOOK_1')}"
GLOBAL_CHAT_WEBHOOK_2 = f"{os.getenv('WEBHOOK_2')}"
GLOBAL_CHAT_CHANNEL = 872195315535601745
GLOBAL_CHAT_CHANNEL_2 = 872206748600131644