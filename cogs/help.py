import discord
from config import MAIN_COLOR, EMOJIS_FOR_COGS
from utils.embeds import error_embed
from discord.ext import commands
import logging
import datetime


async def get_cog_help(cog, context):
    cog = context.bot.get_cog(cog)
    if cog.qualified_name == 'nsfw' and not context.channel.is_nsfw():
        return error_embed(
            "Go away horny!",
            "Please go to a **NSFW** channel"
        )

    embed = discord.Embed(title=f"{cog.qualified_name.title()} Category", color=MAIN_COLOR)

    cmd_info = ""
    cmds = cog.get_commands()

    for info in cmds:
        cmd_info += f"`{context.clean_prefix}{info.name}`\n"

    embed.description = f"To get info help, please use `{context.clean_prefix}help <command>`\n\n**Description:**\n`{cog.description}`\n\n**Commands:**\n{cmd_info}"

    return embed

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        help_reply = self.context
        embed = discord.Embed(title="help command", color=MAIN_COLOR)
        embed.set_footer(text=f"Requested by {self.context.author}", icon_url=self.context.author.avatar.url)
        yes = '\n'.join([f"{EMOJIS_FOR_COGS[cog.qualified_name]}{cog.qualified_name.title()} [ `{len(cmds)}` ]" for cog, cmds in mapping.items() if cog is not None and len(cmds) != 0 and cog.qualified_name.lower() == cog.qualified_name])
        embed.description = f"**Info**:\n `{help_reply.clean_prefix}help <cog>`\n**Prefix**: `{help_reply.clean_prefix}`\n**Cogs**:\n{yes}"
        await help_reply.send(embed=embed)

    async def send_command_help(self, command):
        help_command = self.context.send
        embed = discord.Embed(title="Command Information", color=MAIN_COLOR)
        embed.add_field(name="Usage", value=f"```{self.get_command_signature(command)}```")
        alias = command.aliases
        des = command.description
        time = command._buckets._cooldown
        if alias:
            embed.add_field(name="Aliases", value=f"```{alias}```", inline=False)
        if des:
            embed.add_field(name="Description", value=f"```{des}```", inline=False)
        if time:
            embed.add_field(name="Cooldown", value=f"```{time.per} seconds```", inline=False)
        await help_command(embed=embed)

    async def send_cog_help(self, cog):
        help_cog = self.context
        await help_cog.send(embed=await get_cog_help(cog.qualified_name, help_cog))

    async def send_group_help(self, group: commands.Group):
        prefix = self.context.clean_prefix
        embed = discord.Embed(
            title="Group command information",
            description='\n'.join([f"`{prefix}{command.qualified_name} {command.signature}` - {command.help}" for command in group.commands]),
            color=MAIN_COLOR
        )
        await self.context.reply(embed=embed)


class help_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = MyHelp()

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Help is ready')

def setup(bot):
    bot.add_cog(help_command(bot=bot))
