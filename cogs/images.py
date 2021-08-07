import asyncio
import datetime
import logging
from functools import partial

import discord
from discord.ext import commands

from config import ERROR_COLOR, MAIN_COLOR, VERIFIED, FUN_COLOR
import random
import aiohttp
import io

class images(commands.Cog, description="This is where you can get images"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Images is ready')


    @commands.command()
    async def horny(self, ctx, member: discord.Member = None):
     member = member or ctx.author
     await ctx.trigger_typing()
     async with aiohttp.ClientSession() as session:
        async with session.get(
        f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.url_as(format="png")}') as af:
         if 300 > af.status >= 200:
            fp = io.BytesIO(await af.read())
            file = discord.File(fp, "horny.png")
            em = discord.Embed(
                title="bonk",
                color=0xf1f1f1,
            )
            em.set_image(url="attachment://horny.png")
            await ctx.send(embed=em, file=file)
         else:
            await ctx.send('No horny :(')
        await session.close()

    @commands.command()
    async def pikachu(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://some-random-api.ml/img/pikachu')
       json = await request.json()
       embed = discord.Embed(title="Pika Pika!", color=MAIN_COLOR)
       embed.set_image(url=json['link'])
       await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://some-random-api.ml/img/dog')
       json = await request.json()
       embed = discord.Embed(title="Woof Woof!", color=MAIN_COLOR)
       embed.set_image(url=json['link'])
       await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://some-random-api.ml/img/cat')
       json = await request.json()
       embed = discord.Embed(title="Meow!", color=MAIN_COLOR)
       embed.set_image(url=json['link'])
       await ctx.send(embed=embed)

    @commands.command()
    async def panda(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://some-random-api.ml/img/panda')
       json = await request.json()
       embed = discord.Embed(title="Panda!", color=MAIN_COLOR)
       embed.set_image(url=json['link'])
       await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(images(bot=bot))