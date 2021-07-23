import discord
from discord.ext import commands

class Button(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Hit me', style=discord.ButtonStyle.green)
    async def button_button(self, button, interaction):
        await interaction.response.send_message("Get fucked", ephemeral=True)