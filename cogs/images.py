import logging

import discord
from discord.ext import commands

from config import MAIN_COLOR
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
            async with session.get(f'https://some-random-api.ml/canvas/horny?avatar={member.avatar.replace(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "horny.png")
                    em = discord.Embed(
                        title="bonk",
                        color=MAIN_COLOR,
                    )
                    em.set_image(url="attachment://horny.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No horny :(')
        await session.close()

    @commands.command()
    async def gay(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar.replace(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "gay.png")
                    em = discord.Embed(
                        title="He has came out",
                        color=MAIN_COLOR,
                    )
                    em.set_image(url="attachment://gay.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No gay :(')
        await session.close()

    @commands.command()
    async def jail(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        await ctx.trigger_typing()
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://some-random-api.ml/canvas/jail?avatar={member.avatar.replace(format="png")}') as af:
                if 300 > af.status >= 200:
                    fp = io.BytesIO(await af.read())
                    file = discord.File(fp, "jail.png")
                    em = discord.Embed(
                        title="He be in jail",
                        color=MAIN_COLOR,
                    )
                    em.set_image(url="attachment://jail.png")
                    await ctx.send(embed=em, file=file)
                else:
                    await ctx.send('No jial :(')
        await session.close()

    @commands.command()
    async def comment(self, ctx, *, text=None):
        if text is None:
            await ctx.send("You need to add text to this")
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://some-random-api.ml/canvas/youtube-comment?avatar={ctx.author.avatar.url}&username={ctx.author.name}&comment={text}') as af:
                    if 300 > af.status >= 200:
                        fp = io.BytesIO(await af.read())
                        file = discord.File(fp, "comment.png")
                        em = discord.Embed(
                            title="Comment",
                            color=MAIN_COLOR,
                        )
                        em.set_image(url="attachment://comment.png")
                        await ctx.send(embed=em, file=file)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member):
        if member is None:
            embed = discord.Embed(title=f"Avater of {ctx.author.name}", color=MAIN_COLOR)
            embed.set_image(url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Avatar of {member.name}", color=MAIN_COLOR)
            embed.set_image(url=member.avatar.url)
            await ctx.send(embed=embed)

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
