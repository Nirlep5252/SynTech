import discord
from discord.ext import commands

from config import Website_link

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