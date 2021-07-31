import discord
from discord.ext import commands

from config import Website_link, MAIN_COLOR, VERIFIED, TICKET_EMOJI, CLOSE_EMOJI
from utils.database import db
import random

class Button(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(
            style=discord.ButtonStyle.url,
            label='Website',
            url=Website_link
        ))

    @discord.ui.button(label='Hit me', style=discord.ButtonStyle.green)
    async def button(self, button, interaction):
        await interaction.response.send_message("Get fucked", ephemeral=True)

    @discord.ui.button(label='Don\'t hit me', style=discord.ButtonStyle.green)
    async def button_button(self, button, interaction):
        await interaction.response.send_message("Whyyyyyyyyy", ephemeral=True)

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
        embed = discord.Embed(title="Verified", description=f"You have been Verified, You can now chat with the other developers!", color=MAIN_COLOR).set_footer(text=f"Welcome to the server", icon_url=interaction.user.avatar.url)
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
            embed = discord.Embed(title="Closed", description=f"We hope we fixed your problem!", color=MAIN_COLOR).set_footer(text="If you think this was a mistake dm a staff")
            member = discord.utils.get(interaction.guild.members, id=int(interaction.channel.topic))
            await member.send(embed=embed)
            await interaction.channel.delete()

    @discord.ui.button(label="Report", style=discord.ButtonStyle.green, custom_id="report_view:green")
    async def report(self, button, interaction):
         embed = discord.Embed(title="Report ticket", description="Please give us screenshots and the users id", color=MAIN_COLOR).set_footer(text="If this was by mistake please let us know", icon_url=interaction.user.avatar.url)
         await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Question", style=discord.ButtonStyle.blurple, custom_id="question_view:blurple")
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
         overwrites = {
            interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
            interaction.user: discord.PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
         channel = await interaction.guild.create_text_channel(name=f'ticket-{random.randint(0,1000)}', overwrites=overwrites, topic=interaction.user.id)
         embed = discord.Embed(title="Thank you!", description=f">>> Please Close this ticket if you did not mean to open it.\nPlease hit the report button to report a user.\nPlease hit the question button if you have a question.", color=MAIN_COLOR)
         await channel.send(f"<@{interaction.user.id}>", embed=embed, view=Close())
         tickets = {"ticket_guild_id": interaction.guild.id, "ticket": interaction.user.id}
         db.collection.insert_one(tickets)

        else:
            await interaction.response.send_message("You have a ticket open", ephemeral=True)

