import logging

import discord
from discord.ext import commands

from config import EMOJIS_FOR_COGS, MAIN_COLOR, MONEY_EMOJI
from utils.database import db
import random


class money(commands.Cog, description="Make money then sleep"):
    def __init__(self, bot):
        self.bot = bot
        self.items = {
            "dog": {"prize": 1000, "description": "Buy a cute doggo 🐶", "emoji": "🐶"},
            "cat": {"prize": 1000, "description": "Buy a cute kitten >w<", "emoji": "😺"},
            "blue": {"prize": 69420, "description": "Buy a wild sexy Blue.", "emoji": "<:mmm:842687641639452673>"},
            "avi": {"prize": 69420, "description": "A very cute boi U-U", "emoji": "<a:LeAvi:868476055512555520>"},
            "sans": {"prize": 69420, "description": "Sans-chan!~", "emoji": "<:cat_uwu:856054147693936673>"},
            "nirlep": {"prize": -1, "description": "Ugly person", "emoji": "<:ew:805832225538310145>"},
            "house": {"prize": 10000, "description": "A house for you to live in!", "emoji": "🏠"},
            # add more items here :>
        }

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info('Money is ready')

    @commands.command(help="See what you can buy", name="shop")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _shop(self, ctx: commands.Context):
        embed = discord.Embed(
            title=f"Shop [{len(self.items)}]",
            description="Here's what you can buy",
            colour=MAIN_COLOR,
        ).set_footer(text=f"Use {ctx.clean_prefix}buy <item> to buy an item!")
        for item, stuff in self.items.items():
            embed.add_field(
                name=f"{stuff['emoji']} • {item.title()}",
                value=f"""
**Prize:** {EMOJIS_FOR_COGS['money']} {stuff['prize']}
**Description:** {stuff['description']}
                """
            )
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.member)
    async def work(self, ctx):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            number = random.randint(1, 25)
            responses = ['Coder', "PornStar", "EpicBot Dev", "Dog Walker"]
            jobs = random.choice(responses)
            money = {"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": number, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Work", description=f"You worked as a {jobs} for {number}{MONEY_EMOJI}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            money_number = random.randint(1, 25)
            responses = ['Coder', "PornStar", "EpicBot Dev", "Dog Walker"]
            jobs = random.choice(responses)
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + money_number, "bank": e['bank']}})
            embed = discord.Embed(title="Work", description=f"You worked as a {jobs} for {money_number}{MONEY_EMOJI}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command()
    async def transfer(self, ctx, money_stuff: int):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        all = 0
        if e['money'] >= money_stuff:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] - money_stuff, "bank": e['bank'] + money_stuff}})
            embed = discord.Embed(title="Transfer", description=f"{money_stuff}{MONEY_EMOJI} to your bank account", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e is None:
            ctx.send("No money lol")

        elif money_stuff == all:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] - e['money'], "bank": e['bank'] + e['money']}})
            embed = discord.Embed(title="Transfer", description=f"{money_stuff}{MONEY_EMOJI} to your bank account", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            await ctx.send("You don't have enough money")

    @commands.command()
    async def withdraw(self, ctx, money_stuff: int):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e['bank'] >= money_stuff:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + money_stuff, "bank": e['bank'] - money_stuff}})
            embed = discord.Embed(title="Withdraw", description=f"{money_stuff}{MONEY_EMOJI} to your wallet", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        elif e is None:
            ctx.send("No money lol")

        else:
            await ctx.send("You don't have enough money")

    @commands.command()
    @commands.cooldown(1, 18000, commands.BucketType.member)
    async def rob(self, ctx, member: discord.Member = None):
        a = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        number = 20

        if member is None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("Please ping a user")
            return

        elif member == ctx.author:
            await ctx.send("Please ping a user")
            return

        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": member.id})

        if a is None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("Please open a account by running `!work`")
            return

        if e['money'] >= number:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": member.id}, update={"$set": {"money": e['money'] - number, "bank": e['bank']}})
            await ctx.send(f"You took {number}{MONEY_EMOJI} from {member.name}")
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": a['money'] + number, "bank": a['bank']}})

        elif e is None:
            ctx.command.reset_cooldown(ctx)
            embed = discord.Embed(title="Rob", description=f"{member.name} has no money to take", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            ctx.command.reset_cooldown(ctx)
            await ctx.send(f"{member.name} does not have much money so lets leave them")

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.member)
    async def beg(self, ctx):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            responses = ["Mr.Cat", "Nirlep", "Awoosh", "Avi", "Blue.", "Your Son"]
            response = random.choice(responses)
            number = random.randint(1, 15)
            money = {"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": number}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Beg", description=f"{response} has gave you {number}{MONEY_EMOJI}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            responses = ["Mr.Cat", "Nirlep", "Awoosh", "Avi", "Blue.", "Your Son"]
            names = random.choice(responses)
            money_number = random.randint(1, 15)
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + money_number}})
            embed = discord.Embed(title="Beg", description=f"{names} has gave you {money_number}{MONEY_EMOJI}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command(aliases=['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": member.id})

        if e is None:
            embed = discord.Embed(title=f"Balance For {member.name}", description=f"{member.name} has No money", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f"Balance For {member.name}", description=f"Wallet: {e['money']}{MONEY_EMOJI}\nBank: {e['bank']}{MONEY_EMOJI}", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.member)
    async def daily(self, ctx):
        e = db.collection.find_one({"guild_id": ctx.guild.id, "_user": ctx.author.id})
        if e is None:
            money = {"guild_id": ctx.guild.id, "_user": ctx.author.id, "money": 100}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Daily", description=f"You got 100{MONEY_EMOJI} from your daily", color=MAIN_COLOR)
            await ctx.send(embed=embed)

        else:
            db.collection.update_one(filter={"guild_id": ctx.guild.id, "_user": ctx.author.id}, update={"$set": {"money": e['money'] + 100}})
            embed = discord.Embed(title="Daily", description=f"You got 100{MONEY_EMOJI} from your daily", color=MAIN_COLOR)
            await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def buy(self, ctx):
        await ctx.send("this is WIP")


def setup(bot):
    bot.add_cog(money(bot=bot))
