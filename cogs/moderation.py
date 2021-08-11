import logging

import asyncio
from datetime import datetime

import discord
from discord.ext import commands

from utils.database import db
from config import MAIN_COLOR, ERROR_COLOR, WARN_COLOR, LOG_CHANNEL, GLOBAL_CHAT_WEBHOOK, GLOBAL_CHAT_WEBHOOK_2, GLOBAL_CHAT_CHANNEL, GLOBAL_CHAT_CHANNEL_2, PREFIXES
from discord import Webhook
import aiohttp

class moderation(commands.Cog, description="This is the cog that allows you to get rid of bad boys"):
    def __init__(self, bot):
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
    async def on_message(self, message):
      if message.author.bot:
          return

      elif f"!" in message.content:
           return

      elif message.channel.id == GLOBAL_CHAT_CHANNEL:
        async with aiohttp.ClientSession() as session:
             webhook = Webhook.from_url(GLOBAL_CHAT_WEBHOOK, session=session)
             await webhook.send(message.content, username=message.author.name, avatar_url=message.author.avatar.url)

      elif message.channel.id == GLOBAL_CHAT_CHANNEL_2:
        async with aiohttp.ClientSession() as session:
             webhook = Webhook.from_url(GLOBAL_CHAT_WEBHOOK_2, session=session)
             await webhook.send(message.content, username=message.author.name, avatar_url=message.author.avatar.url)

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
                                  description=f"Sorry but no",
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
    async def clearwarns(self, ctx, member: discord.Member=None):
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
    async def rwarn(self, ctx, number: int, member: discord.Member=None):
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
            update={"$set": {"warnings": warnings}})
            embed = discord.Embed(title="Removed", description=f"{member.name} has one warn removed", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def warns(self, ctx, member: discord.Member=None):
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
            await member.send(f'You were kicked from {ctx.guild.name}')
            await member.kick(reason=reason)
            await ctx.send(f'{member} was kicked.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
            await member.send(f'You were banned from {ctx.guild.name}')
            await member.ban(reason=reason)
            await ctx.send(f'{member} was banned.')

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

def setup(bot):
    bot.add_cog(moderation(bot=bot))