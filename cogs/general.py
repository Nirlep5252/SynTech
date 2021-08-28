import asyncio
import logging

import discord
from discord.ext import commands

from config import ERROR_COLOR, MAIN_COLOR, FUN_COLOR, CHAT_BOT_CHANNEL, BAD_WORDS
import random
import aiohttp
from utils.button import Counter, Pages
from utils.database import db
from animec import Aninews
import os

news = Aninews()

class general(commands.Cog, description="This well be where all fun commands are"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('General is ready')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.channel.id == CHAT_BOT_CHANNEL:
         async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.monkedev.com/fun/chat?msg={message.content}')
            json = await request.json()
            await message.reply(f"{json['response']}")


    @commands.command()
    async def remindme(self, ctx, time, *, reminder):
        embed = discord.Embed(color=ERROR_COLOR)
        embed.set_footer(
            text="usage !remindme <time> <reminder>",
            icon_url=f"{self.bot.user.avatar.url}")
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning',
                            value='Please specify what do you want me to remind you about.')
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"
        if seconds == 0:
            embed.add_field(name='Warning',
                            value='Please specify a proper duration')
        elif seconds < 300:
            embed.add_field(name='Warning',
                            value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
        elif seconds > 7776000:
            embed.add_field(name='Warning',
                            value='You have specified a too long duration!\nMaximum duration is 90 days.')
        else:
            await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
            await asyncio.sleep(seconds)
            await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
            return
        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."
        ]
        response = random.choice(responses)
        embed = discord.Embed(title="8ball", description=f"Question: {question}\nAnswer: {response}", color=FUN_COLOR)
        await ctx.send(embed=embed)

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason):
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for("raw_reaction_add", timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command()
    async def reverse(self, ctx, *, text: str):
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command(name="anime-quote")
    async def anime_quote(self, ctx):
        async with aiohttp.ClientSession() as session:
            request = await session.get('https://some-random-api.ml/animu/quote')
            json = await request.json()
            embed = discord.Embed(title=f"Quote from {json['anime']}", description=f"Characther: {json['characther']}\nQuote: {json['sentence']}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command()
    async def count(self, ctx):
        await ctx.send("Hit the button to count", view=Counter(ctx))

    @commands.command(name="anime-news")
    async def anime_news(self, ctx):
        embed = discord.Embed(title="Home Page", description="Go to the next page for anime", color=MAIN_COLOR)
        embeds = [(discord.Embed(title=f"{news.titles[i]}", description=f"{news.description[i]}", color=MAIN_COLOR)) for i in range(0, len(news.titles))]
        await ctx.send(embed=embed, view=Pages(ctx, embeds))

    @commands.command()
    async def chat(self, ctx, *, text=None):
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://api.monkedev.com/fun/chat?msg={text}')
            json = await request.json()
            await ctx.reply(f"{json['response']}")

def setup(bot):
    bot.add_cog(general(bot=bot))