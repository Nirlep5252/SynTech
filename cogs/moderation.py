import logging

import asyncio
import discord
from discord.ext import commands

from utils.database import db
from config import MAIN_COLOR, ERROR_COLOR, WARN_COLOR
from config import Config as config

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.developers = config.DEVELOPERS

    async def developer_check(ctx):
       return ctx.author.id in config.DEVELOPERS

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('General is ready')

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
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member, *, reason="Reason was not given"):
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

        e = db.collection.find_one(
                {"_id": member.id})

        if e is None:
                warns = {"_id": member.id, "warnings": 1}
                db.collection.insert_one(warns)
                embed = discord.Embed(title="Warning", description=f"You were warned in {ctx.guild.name} for {reason}", color=MAIN_COLOR)
                await ctx.send(f'you warned {member.name}')
                await member.send(embed=embed)

        elif 3 <= e['warnings'] < 7:
            db.collection.update_one(
                    filter={"_id": member.id},
                    update={"$set": {"warnings":  e['warnings'] + 1}}
                )
            await member.send(f'You were kicked from {ctx.guild.name}')
            await member.kick(reason=reason)
            await ctx.send(f'{member.name} was kicked.')
        elif e['warnings'] >= 7:
            a = db.collection.find_one({"_id": member.id, "warnings": e['warnings']})
            await member.send(f'You were banned from {ctx.guild.name}')
            await member.ban(reason=reason)
            await ctx.send(f'{member} was banned.')
            db.collection.delete_one(a)

        else:
            db.collection.update_one(
                    filter={"_id": member.id},
                    update={"$set": {"warnings":  e['warnings'] + 1}}
                )
            embed = discord.Embed(title="Warning", description=f"You were warned in {ctx.guild.name} for {reason}", color=MAIN_COLOR)
            await ctx.send(f'warn was added to {member.name}')
            await member.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def rwarn(self, ctx, member: discord.Member):

        e = db.collection.find_one(
            {"_id": member.id})

        if e is None:
              await ctx.send(f"{member.name} has no warnings")

        elif e['warnings'] == 0:
            await ctx.send(f"{member.name} has no warnings")
            return

        else:
            db.collection.update_one(
                filter={"_id": member.id},
                update={"$set": {"warnings": e['warnings'] - 1}}
            )
            await ctx.send(f'{member.name} has one less warn')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def warns(self, ctx, member: discord.Member):
        e = db.collection.find_one({"_id": member.id})

        if e is None:
               embed = discord.Embed(title="Warnings", description="You have no warnings", color=MAIN_COLOR)
               await ctx.send(embed=embed)

        elif e['warnings'] == 0:
            embed = discord.Embed(title="Warnings", description="You have no warnings", color=MAIN_COLOR)
            await ctx.send(embed=embed)
            return

        else:
            embed = discord.Embed(title="Warnings", description=f"You have {e['warnings']} warnings", color=WARN_COLOR)
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



