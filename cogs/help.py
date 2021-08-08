import discord
from config import MAIN_COLOR, Website_link
from discord.ext import commands
import logging

async def get_cog_help(cog, context):
    cog = context.bot.get_cog(cog)

    embed = discord.Embed(title=f"{cog.qualified_name.title()} Category", color=MAIN_COLOR)

    cmd_info = ""
    cmds = cog.get_commands()

    for info in cmds:
        cmd_info += f"`{context.clean_prefix}{info.name}`\n"

    embed.description = f"To get info help, please use `{context.clean_prefix}help <command>`\n\n**Description:**\n`{cog.description}`\n\n**Commands:**\n{cmd_info}"

    return embed

class EpicBotHelpSelect(discord.ui.Select):
    def __init__(self, placeholder, options, ctx):
        super().__init__(
            placeholder=placeholder,
            options=options
        )
        self.ctx = ctx

    async def callback(self, i):
        await i.response.send_message(embed=await get_cog_help(
            self.values[0], self.ctx
        ), ephemeral=True)
class MyHelp(commands.HelpCommand):

    async def send_bot_help(self, mapping):
        help_reply = self.context
        embed = discord.Embed(title="help command", color=MAIN_COLOR)
        embed.set_thumbnail(url=self.context.bot.user.avatar.url)
        embed.set_footer(text=f"Requested by {self.context.author}", icon_url=self.context.author.avatar.url)
        embed.add_field(name="Prefix", value=f"`{help_reply.clean_prefix}`", inline=False)
        embed.add_field(name="Commands", value=f"{len(help_reply.bot.commands)} Commands", inline=False)
        for cog, cmds in mapping.items():
         if cog is not None and cog.qualified_name.lower() == cog.qualified_name:
              value = f', {help_reply.clean_prefix}'.join([cmd.name for cmd in cmds])
              if len(cmds) != 0:
                embed.add_field(
                    name=f"{cog.qualified_name.title()}",
                    value=f"{help_reply.clean_prefix}{value}",
                    inline=False
                    )
              else:
                pass

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

class help_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = MyHelp()

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Help is ready')

def setup(bot):
    bot.add_cog(help_command(bot=bot))