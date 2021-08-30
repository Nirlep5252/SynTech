import discord
from discord.ext import commands

from config import Website_link, MAIN_COLOR, VERIFIED, TICKET_EMOJI, CLOSE_EMOJI, TICKETS_CATEGORY, STAFF_ROLE, FORWARD_ARROW, BACK_ARROW, MONEY_EMOJI
from utils.database import db
from typing import List
import random
from utils.embeds import custom_embed


class Button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.url,
            label='Website',
            url=Website_link
        ))


class Verify(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.bot = discord.Client

    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, emoji=f"{VERIFIED}", custom_id="verify_view:green")
    async def verify(self, button, interaction):
        role = interaction.guild.get_role(870159097524273262)
        member_role = interaction.guild.get_role(870161379141763092)
        await interaction.user.add_roles(role)
        await interaction.user.add_roles(member_role)
        embed = discord.Embed(title="Verified", description="You have been Verified, You can now chat with the other developers!", color=MAIN_COLOR).set_footer(text="Welcome to the server", icon_url=interaction.user.avatar.url)
        welcome = interaction.guild.get_channel(867935486298177606)
        welcome_embed = discord.Embed(title="Welcome", description=f"Hey guys welcome {interaction.user.name} to the server!", color=MAIN_COLOR).set_footer(text="Welcome to the server", icon_url=interaction.user.avatar.url)
        await welcome.send(embed=welcome_embed)
        await interaction.user.send(embed=embed)


class Close(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, emoji=f"{CLOSE_EMOJI}", custom_id="close_view:red")
    async def close(self, button, interaction):
        e = db.collection.find_one(
            {"ticket_guild_id": interaction.guild.id, "ticket": int(interaction.channel.topic)})
        if e is None:
            await interaction.response.send_message("User has no ticket", ephemeral=True)

        else:
            a = db.collection.find_one({"ticket_guild_id": interaction.guild.id, "ticket": int(interaction.channel.topic)})
            db.collection.delete_one(a)
            embed = discord.Embed(title="Closed", description="We hope we fixed your problem!", color=MAIN_COLOR).set_footer(text="If you think this was a mistake dm a staff")
            member = discord.utils.get(interaction.guild.members, id=int(interaction.channel.topic))
            await member.send(embed=embed)
            await interaction.channel.delete()

    @discord.ui.button(label="Report", style=discord.ButtonStyle.green, disabled=False, custom_id="report_view:green")
    async def report(self, button, interaction):
        embed = discord.Embed(title="Report ticket", description="Please give us screenshots and the users id", color=MAIN_COLOR).set_footer(text="If this was by mistake please let us know", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Question", style=discord.ButtonStyle.blurple, disabled=False, custom_id="question_view:blurple")
    async def question(self, button, interaction):
        embed = discord.Embed(title="Question ticket", description="We will try our best to answer your question", color=MAIN_COLOR).set_footer(text="If this was by mistake please let us know", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.green, emoji=f"{TICKET_EMOJI}", custom_id="ticket_view:green")
    async def ticket(self, button, interaction):
        e = db.collection.find_one({"ticket_guild_id": interaction.guild.id, "ticket": interaction.user.id})
        if e is None:
            tickets_thing = discord.utils.get(interaction.guild.categories, id=TICKETS_CATEGORY)
            overwrites = {
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
                interaction.user: discord.PermissionOverwrite(read_messages=True),
                interaction.guild.get_role(STAFF_ROLE): discord.PermissionOverwrite(read_messages=True),
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
            }
            channel = await interaction.guild.create_text_channel(name=f'ticket-{random.randint(0,1000)}', category=tickets_thing, overwrites=overwrites, topic=interaction.user.id)
            embed = discord.Embed(title="Thank you!", description=">>> Please close this ticket if you did not mean to open it.\nPlease hit the report button to report a user.\nPlease hit the question button if you have a question.", color=MAIN_COLOR)
            await channel.send(f"<@{interaction.user.id}>, I will ping the <@&{STAFF_ROLE}>", embed=embed, view=Close())
            tickets = {"ticket_guild_id": interaction.guild.id, "ticket": interaction.user.id}
            db.collection.insert_one(tickets)

        else:
            await interaction.response.send_message("You have a ticket open", ephemeral=True)


class Menu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Info", style=discord.ButtonStyle.blurple)
    async def menu(self, button, interaction):
        embed = discord.Embed(title="Info", description="To get info on a cog just do `!help <cog name>`", color=MAIN_COLOR)
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="delete", style=discord.ButtonStyle.red)
    async def delete(self, button, interaction):
        await interaction.message.delete()


class Pages(discord.ui.View):
    def __init__(self, ctx: commands.Context, embeds: List[discord.Embed]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds
        self.current = 0

    async def edit(self, msg, pos):
        em = self.embeds[pos]
        em.set_footer(text=f"Page: {pos+1}")
        await msg.edit(embed=em)

    @discord.ui.button(emoji=f'{BACK_ARROW}', style=discord.ButtonStyle.blurple)
    async def bac(self, b, i):
        if self.current == 0:
            return
        await self.edit(i.message, self.current - 1)
        self.current -= 1

    @discord.ui.button(emoji="🏠", style=discord.ButtonStyle.blurple)
    async def home(self, button, interaction):
        embed = custom_embed(
            "Home Page",
            "Go to the next page for anime"
        )
        await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(emoji=f'{FORWARD_ARROW}', style=discord.ButtonStyle.blurple)
    async def nex(self, b, i):
        if self.current + 1 == len(self.embeds):
            return
        await self.edit(i.message, self.current + 1)
        self.current += 1

    async def interaction_check(self, interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command", ephemeral=True)


class Counter(discord.ui.View):
    def __init__(self, ctx, *, timeout=None):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    @discord.ui.button(label='0', style=discord.ButtonStyle.red)
    async def count(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label) if button.label else 0
        if number + 1 >= 999:
            button.style = discord.ButtonStyle.green
            button.disabled = True
        button.label = str(number + 1)

        await interaction.response.edit_message(view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command", ephemeral=True)

class Search(discord.ui.View):
    def __init__(self, ctx, *, timeout=180.0):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="House", style=discord.ButtonStyle.blurple)
    async def house(self, button: discord.ui.Button, interaction: discord.Interaction):
        e = db.collection.find_one({"guild_id": interaction.guild.id, "_user": interaction.user.id})
        if e is None:
            number = random.randint(15, 800)
            money = {"guild_id": interaction.guild.id, "_user": interaction.user.id, "money": number, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="House", description=f"You found {MONEY_EMOJI} {number} from a house", color=MAIN_COLOR)
            await interaction.response.send_message(embed=embed)
            for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)

        elif e['bank'] is None:
         await interaction.response.send_message("You need a bank account", ephemeral=True)
        for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)

        else:
            number = random.randint(15, 800)
            db.collection.update_one(filter={"guild_id": interaction.guild.id, "_user": interaction.user.id}, update={"$set": {"money": e['money'] + number, "bank": e['bank']}})
            embed = discord.Embed(title="House", description=f"You found {MONEY_EMOJI} {number} from a house", color=MAIN_COLOR)
            await interaction.response.send_message(embed=embed)
            for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)

    @discord.ui.button(label="Dumpster", style=discord.ButtonStyle.red)
    async def dumpster(self, button: discord.ui.Button, interaction: discord.Interaction):
        e = db.collection.find_one({"guild_id": interaction.guild.id, "_user": interaction.user.id})
        if e is None:
            number = random.randint(15, 1000)
            money = {"guild_id": interaction.guild.id, "_user": interaction.user.id, "money": number, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Dumpster", description=f"You found {MONEY_EMOJI} {number} from a Dumpster", color=MAIN_COLOR)
            await interaction.response.send_message(embed=embed)
            for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)

        elif e['bank'] is None:
         await interaction.response.send_message("You need a bank account", ephemeral=True)
         for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)

        else:
            number = random.randint(15, 1000)
            db.collection.update_one(filter={"guild_id": interaction.guild.id, "_user": interaction.user.id}, update={"$set": {"money": e['money'] + number, "bank": e['bank']}})
            embed = discord.Embed(title="Dumpster", description=f"You found {MONEY_EMOJI} {number} from a Dumpster", color=MAIN_COLOR)
            await interaction.response.send_message(embed=embed)
            for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)

    @discord.ui.button(label="Nirleps House", style=discord.ButtonStyle.red)
    async def hose2(self, button: discord.ui.Button, interaction: discord.Interaction):
        e = db.collection.find_one({"guild_id": interaction.guild.id, "_user": interaction.user.id})
        if e is None:
            number = random.randint(15, 700)
            money = {"guild_id": interaction.guild.id, "_user": interaction.user.id, "money": number, "bank": 0}
            db.collection.insert_one(money)
            embed = discord.Embed(title="Dumpster", description=f"You found {MONEY_EMOJI} {number} in Nirleps House", color=MAIN_COLOR)
            await interaction.response.send_message(embed=embed)
            for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)

        elif e['bank'] is None:
         await interaction.response.send_message("You need a bank account", ephemeral=True)
         for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)

        else:
            number = random.randint(15, 700)
            db.collection.update_one(filter={"guild_id": interaction.guild.id, "_user": interaction.user.id}, update={"$set": {"money": e['money'] + number, "bank": e['bank']}})
            embed = discord.Embed(title="Dumpster", description=f"You found {MONEY_EMOJI} {number} in Nirleps House", color=MAIN_COLOR)
            await interaction.response.send_message(embed=embed)
            for item in self.children:
             item.disabled = True
             await interaction.message.edit(view=self)


    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command", ephemeral=True)


class LeaderboardView(discord.ui.View):
    def __init__(self, ctx: commands.Context, embed1: discord.Embed, embed2: discord.Embed):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embed1 = embed1
        self.embed2 = embed2

    @discord.ui.button(label="Server Leaderboard", style=discord.ButtonStyle.blurple, disabled=True)
    async def guild_leaderboard(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.children[1].disabled = False
        button.disabled = True
        await interaction.message.edit(embed=self.embed1, view=self)

    @discord.ui.button(label="Global Leaderboard", style=discord.ButtonStyle.blurple)
    async def global_leaderboard(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.children[0].disabled = False
        button.disabled = True
        await interaction.message.edit(embed=self.embed2, view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command", ephemeral=True)
