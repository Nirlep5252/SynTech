import discord
from config import MAIN_COLOR
from discord.ext import commands

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

class help_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = MyHelp()

def setup(bot):
    bot.add_cog(help_command(bot=bot))