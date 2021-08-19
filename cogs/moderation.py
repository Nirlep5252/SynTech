import logging

import asyncio
from main import get_prefix

import discord
from discord.ext import commands

from utils.database import db, prefix_collection
from config import (
    MAIN_COLOR, ERROR_COLOR, WARN_COLOR, LOG_CHANNEL,
    GLOBAL_CHAT_WEBHOOK, GLOBAL_CHAT_WEBHOOK_2, GLOBAL_CHAT_CHANNEL,
    GLOBAL_CHAT_CHANNEL_2
)
from discord import Webhook
import aiohttp
import time


class moderation(commands.Cog, description="This is the cog that allows you to get rid of bad boys"):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Moderation is ready')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        channel = self.bot.get_channel(LOG_CHANNEL)
        embed = discord.Embed(title="Command Used!", description=f"**Command:**\n```{ctx.message.content}```\n**Guild:**\n```{ctx.guild.name} - {ctx.guild.id}```\n**Channel:**\n```{ctx.channel.name} - {ctx.channel.id}```\n**User:**\n```{ctx.author.name} - {ctx.author.id}```", timestamp=discord.utils.utcnow(), color=MAIN_COLOR).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        result = db.collection.find_one({"_guild_id": member.guild.id})

        if not result:
            return

        if "alt" not in result:
            return

        if result['alt']:
            print("On")
            if time.time() - member.created_at.timestamp() < 2492000:
                channel = self.bot.get_channel(LOG_CHANNEL)
                embed = discord.Embed(title="Anti Alt", description=f"The user `{member.name}` is an alt account", color=ERROR_COLOR)
                await channel.send(embed=embed)
            else:
                print("acc old")

        else:
            print("Off")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        h = db.logs_collection.find_one({"_id": guild.id})
        if h is None:
           return
        else:
         db.logs_collection.delete_one(h)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        elif "!" in message.content:
            return

        elif message.channel.id == GLOBAL_CHAT_CHANNEL:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(GLOBAL_CHAT_WEBHOOK, session=session)
                await webhook.send(message.content, username=message.author.name, avatar_url=message.author.avatar.url)

        elif message.channel.id == GLOBAL_CHAT_CHANNEL_2:
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(GLOBAL_CHAT_WEBHOOK_2, session=session)
                await webhook.send(message.content, username=message.author.name, avatar_url=message.author.avatar.url)

    @commands.Cog.listener("on_message")
    async def prefix_reply(self, message: discord.Message):
        if message.author.bot:
            return
        bot_id = self.bot.user.id
        if message.content.lower() in [f'<@{bot_id}>', f'<@!{bot_id}>']:
            prefixes = await get_prefix(self.bot, message)
            return await message.reply(
                'My prefixes are: ' + ', '.join([f"`{prefix}`" for prefix in prefixes])
            )

    @commands.group(
        aliases=['prefix', 'changeprefix', 'set-prefix', 'set_prefix', 'prefixes'],
        help="Manage the prefixes of your guild!"
    )
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @setprefix.command(help="Add a prefix!")
    async def add(self, ctx: commands.Context, *, prefix: str = None):
        if not prefix:
            return await ctx.reply(f"Please enter a prefix.\nCorrect Usage: `{ctx.clean_prefix}prefix add <prefix>`")
        document = prefix_collection.find_one({"_id": ctx.guild.id})
        if not document:
            prefix_collection.insert_one({
                "_id": ctx.guild.id,
                "prefixes": [prefix, ctx.clean_prefix]
            })
            return await ctx.reply(f"The prefix `{prefix}` has been added.")
        else:
            if prefix in document['prefixes']:
                return await ctx.reply(f"The prefix `{prefix}` is already added.")
            if len(document['prefixes']) >= 10:
                return await ctx.reply("You can only have 10 prefixes.")
            else:
                prefix_collection.update_one(
                    {"_id": ctx.guild.id},
                    {"$push": {"prefixes": prefix}}
                )
                return await ctx.reply(f"The prefix `{prefix}` has been added.")

    @setprefix.command(help="Remove a prefix!")
    async def remove(self, ctx: commands.Context, *, prefix: str = None):
        if not prefix:
            return await ctx.reply(f"Please enter a prefix.\nCorrect Usage: `{ctx.clean_prefix}prefix remove <prefix>`")
        document = prefix_collection.find_one({"_id": ctx.guild.id})
        if not document:
            return await ctx.reply("There are no prefixes to remove.")
        else:
            if prefix in document['prefixes']:
                prefix_collection.update_one(
                    {"_id": ctx.guild.id},
                    {"$pull": {"prefixes": prefix}}
                )
                return await ctx.reply(f"The prefix `{prefix}` has been removed.")
            else:
                return await ctx.reply(f"The prefix `{prefix}` is not added.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def lock(self, ctx, channel: discord.TextChannel):
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f'{channel.mention} is now locked.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def unlock(self, ctx, channel: discord.TextChannel):
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f'{channel.mention} is now unlocked.')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member, *, reason="No reason was given"):
        if member == ctx.author:
            embed = discord.Embed(title="Oh no",
                                  description="Sorry but no",
                                  color=ERROR_COLOR)
            await ctx.send(embed=embed)
            return

        if member.id == 754432225163870309:
            embed = discord.Embed(description="How **could** you", color=ERROR_COLOR)
            await ctx.send(embed=embed)
            return

        e = db.collection.find_one({"_guild": ctx.guild.id, "_id": member.id})

        if e is None:
            db.collection.insert_one({"_guild": ctx.guild.id, "_id": member.id, "warnings": {"1": reason}})
            embed = discord.Embed(title="Warning", description=f"You were warned in {ctx.guild.name} for {reason}", color=MAIN_COLOR)
            warning = discord.Embed(title="Warned", description=f"You have warned {member.name} for {reason}", color=MAIN_COLOR)
            await ctx.send(embed=warning)
            await member.send(embed=embed)

        else:
            warnings = e['warnings']
            warnings.update({f"{1 if len(warnings) == 0 else max([int(i) for i in warnings]) + 1}": reason})
            db.collection.update_one(filter={"_id": member.id, "_guild": ctx.guild.id}, update={"$set": {"warnings": warnings}})
            embed = discord.Embed(title="Warning", description=f"You were warned in {ctx.guild.name} for {reason}", color=MAIN_COLOR)
            warning_added = discord.Embed(title="Warned Added", description=f"You warned {member.name} for {reason}", color=MAIN_COLOR)
            await ctx.send(embed=warning_added)
            await member.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    @commands.guild_only()
    async def clearwarns(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        e = db.collection.find_one({"_guild": ctx.guild.id, "_id": member.id})

        if e is None:
            await ctx.send(f"{member.name} has no warnings")

        else:
            a = db.collection.find_one({"_guild": ctx.guild.id, "_id": member.id, "warnings": e['warnings']})
            db.collection.delete_one(a)
            await ctx.send(f'{member.name} Has been cleared')

    @commands.command(aliases=["remove-warn"])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def rwarn(self, ctx, number: int, member: discord.Member = None):
        member = member or ctx.author
        e = db.collection.find_one(
            {"_guild": ctx.guild.id, "_id": member.id})

        if e is None:
            await ctx.send(f"{member.name} has no warnings")

        else:
            warnings = e['warnings']
            warnings.pop(str(number))
            db.collection.update_one(
                filter={"_id": member.id, "_guild": ctx.guild.id},
                update={"$set": {"warnings": warnings}}
            )
            embed = discord.Embed(title="Removed", description=f"{member.name} has one warn removed", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def warns(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        e = db.collection.find_one({"_guild": ctx.guild.id, "_id": member.id})
        if e is None:
            embed = discord.Embed(title="Warnings", description=f"{member.name} have no warnings", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            warnings = e['warnings']
            sexy = ',\n'.join([f"`{number}.` - {warnings[number]}" for number in warnings])
            embed = discord.Embed(title=f"Warn(s) for {member.name}", description=f"{sexy}", timestamp=discord.utils.utcnow(), color=WARN_COLOR).set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            await ctx.send(embed=embed)

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)  # +1 is so it deletes the ctx.message
        response_message = await ctx.send(f'{amount} messages were cleared.')
        await asyncio.sleep(5)
        await response_message.delete()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        h = db.logs_collection.find_one({"_id": ctx.guild.id})
        if h is None:
            embed = discord.Embed(title="Kicked!", description=f"I have kicked {member.name} but i could not log the kick please run `{ctx.clean_prefix}setlogs add <channel>`", color=MAIN_COLOR)
            await ctx.send(embed=embed)
            await member.send(f'You were kicked from {ctx.guild.name}')
            await member.kick(reason=reason)
            #await ctx.send(f'{member} was kicked.')
        else:
            channel = self.bot.get_channel(h['channel'])    
            embed = discord.Embed(title="Kicked!", description=f"```User: {member.name}\nStaff: {ctx.author.name}\nReason: {reason}```", color=MAIN_COLOR)
            await channel.send(embed=embed)
            await member.send(f'You were kicked from {ctx.guild.name}')
            await member.kick(reason=reason)
            await ctx.send(f'{member.name} was kicked.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        h = db.logs_collection.find_one({"_id": ctx.guild.id})
        if h is None:
            embed = discord.Embed(title="banned!", description=f"I have banned {member.name} but i could not log the kick please run `{ctx.clean_prefix}setlogs add <channel>`", color=MAIN_COLOR)
            await ctx.send(embed=embed)
            await member.send(f'You were banned from {ctx.guild.name}')
            await member.ban(reason=reason)
        else:
            channel = self.bot.get_channel(h['channel'])    
            embed = discord.Embed(title="Banned!", description=f"```User: {member.name}\nStaff: {ctx.author.name}\nReason: {reason}```", color=MAIN_COLOR)
            await channel.send(embed=embed)
            await member.send(f'You were banned from {ctx.guild.name}')
            await member.ban(reason=reason)
            await ctx.send(f'{member.name} was banned.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def unban(self, ctx, member):
        banned_users = await ctx.guild.banned_users
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{member} is unbanned')

    @commands.group(name="anti-alt", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def anti_alt(self, ctx):
        embed = discord.Embed(title="Anti-Alt", description=f"WOW {self.bot.user.name} now has anti-alt this is great make use to use this well", color=MAIN_COLOR)
        await ctx.send(embed=embed, delete_after=5)
        await asyncio.sleep(5)
        embed_help = discord.Embed(title="Help", description=f"Info: Too use anti-alt do `{ctx.clean_prefix}anti-alt true` and to turn it off do `{ctx.clean_prefix}anit-alt false`", color=MAIN_COLOR)
        await ctx.send(embed=embed_help)

    @anti_alt.command(name="true")
    @commands.has_permissions(administrator=True)
    async def _true(self, ctx):
        e = db.collection.find_one({"_guild_id": ctx.guild.id})

        if e is None:
            db.collection.insert_one({"_guild_id": ctx.guild.id, "alt": True})
            await ctx.send("Anit-alt is now True")

        else:
            db.collection.update_one(filter={"_guild_id": ctx.guild.id}, update={"$set": {"alt": True}})
            await ctx.send("Anit-alt is now on")

    @anti_alt.command(name="false")
    @commands.has_permissions(administrator=True)
    async def _false(self, ctx):
        e = db.collection.find_one({"_guild_id": ctx.guild.id})

        if e is None:
            db.collection.insert_one({"_guild_id": ctx.guild.id, "alt": False})
            await ctx.send("Anit-alt is now off")

        else:
            db.collection.update_one(filter={"_guild_id": ctx.guild.id}, update={"$set": {"alt": False}})
            await ctx.send("Anit-alt is now off")

    @commands.group( invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def setlogs(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(ctx.command)

    @setlogs.command()
    @commands.has_permissions(manage_channels=True)
    async def add(self, ctx, channel: discord.TextChannel):
        channel_id = channel.id
        e = db.logs_collection.find_one(
                {"_id": ctx.guild.id})

        if e is None:
                postchannel = {"_id": ctx.guild.id, "channel": channel_id}
                db.logs_collection.insert_one(postchannel)
                embed = discord.Embed(title="Logs!", description=f'You set `{channel.name}` as your logs channel', color=MAIN_COLOR)
                await ctx.send(embed=embed)

        else:
            db.logs_collection.update_one(
                    filter={"_id": ctx.guild.id},
                    update={"$set": {"channel": channel_id}}
                )
            embed = discord.Embed(title="Logs!", description=f'You set `{channel.name}` as your logs channel', color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @setlogs.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def remove(self, ctx):
        h = db.logs_collection.find_one({"_id": ctx.guild.id})

        if h is None:
            await ctx.send("You have not set a logs channel")

        else:
         await ctx.send(f"The channel <#{h['channel']}> is no longer your logs channel")
         db.logs_collection.delete_one(h)

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def config(self, ctx): #command not working idk why it isn't
        h = db.logs_collection.find_one({"_id": ctx.guild.id})

        if h is None:
            embed = discord.Embed(f"Config for {ctx.guild.name}", description=f"Logs Channel: No channel for logs set yet.", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(f"Config for {ctx.guild.name}", description=f"Logs Channel: `<#{h['channel']}>`", color=MAIN_COLOR)
            await ctx.send(embed=embed)                

def setup(bot):
    bot.add_cog(moderation(bot=bot))
