from config import NSFW_COLOR
import logging
import aiohttp
import discord
from discord.ext import commands

import random

class nsfw(commands.Cog, description="18+ Boys"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Nsfw is ready')

    @commands.command(description='You can see a ||pussy|| with this')
    @commands.is_nsfw()
    async def pussy(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekobot.xyz/api/image?type=pussy')
       json = await request.json()
       embed = discord.Embed(title="Pussy!", color=NSFW_COLOR)
       embed.set_image(url=json['message'])
       await ctx.send(embed=embed)

    @commands.command(description='You can see someones ||feet||')
    @commands.is_nsfw()
    async def feet(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/feet')
       json = await request.json()
       embed = discord.Embed(title="Feet!", color=NSFW_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='You can see someone ||cum||')
    @commands.is_nsfw()
    async def cum(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekos.life/api/v2/img/cum')
       json = await request.json()
       embed = discord.Embed(title="Cum!", color=NSFW_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='You know what this is', aliases=["bj"])
    @commands.is_nsfw()
    async def blowjob(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekobot.xyz/api/image?type=blowjob')
       json = await request.json()
       embed = discord.Embed(title="Blow Job!", color=NSFW_COLOR)
       embed.set_image(url=json['message'])
       await ctx.send(embed=embed)

    @commands.command(description='Boobiesssss')
    @commands.is_nsfw()
    async def boobs(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekobot.xyz/api/image?type=boobs')
       json = await request.json()
       embed = discord.Embed(title="Boobies!", color=NSFW_COLOR)
       embed.set_image(url=json['message'])
       await ctx.send(embed=embed)

    @commands.command(description='Nice')
    @commands.is_nsfw()
    async def ass(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekobot.xyz/api/image?type=ass')
       json = await request.json()
       embed = discord.Embed(title="Nice Ass!", color=NSFW_COLOR)
       embed.set_image(url=json['message'])
       await ctx.send(embed=embed)

    @commands.command(description='Ooh noo')
    @commands.is_nsfw()
    async def anal(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekobot.xyz/api/image?type=anal')
       json = await request.json()
       embed = discord.Embed(title="That most hurt!", color=NSFW_COLOR)
       embed.set_image(url=json['message'])
       await ctx.send(embed=embed)

    @commands.command(description='Yess!')
    @commands.is_nsfw()
    async def hentai(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://shiro.gg/api/images/nsfw/hentai')
       json = await request.json()
       embed = discord.Embed(title="hentai!", color=NSFW_COLOR)
       embed.set_image(url=json['url'])
       await ctx.send(embed=embed)

    @commands.command(description='Here you go')
    @commands.is_nsfw()
    async def holo(self, ctx):
      async with aiohttp.ClientSession() as session:
       request = await session.get('https://nekobot.xyz/api/image?type=holo')
       json = await request.json()
       embed = discord.Embed(title="Holo!", color=NSFW_COLOR)
       embed.set_image(url=json['message'])
       await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def fuck(self, ctx, member: discord.Member=None):
       if member == None:
           embed = discord.Embed(title="oh no", description=f"You need to ping someone", color=NSFW_COLOR)
           await ctx.send(embed=embed)
       else:
          async with aiohttp.ClientSession() as session:
           request = await session.get('https://purrbot.site/api/img/nsfw/fuck/gif')
           json = await request.json()
           embed = discord.Embed(title="WEW!", description=f"{ctx.author.name} fucked {member.name}", color=NSFW_COLOR)
           embed.set_image(url=json['link'])
           await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(nsfw(bot=bot))