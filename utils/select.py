import discord


class Select(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.select(
        placeholder="Please select one",
        options=[
            discord.SelectOption(label='no'),
            discord.SelectOption(label='yes'),
            discord.SelectOption(label='maybe')
        ]
    )
    async def select(self, select, interaction):
        if select.values[0] == "yes":
            await interaction.response.send_message(f"You picked {select.values[0]}", ephemeral=True)
        if select.values[0] == "no":
            await interaction.response.send_message(f"You picked1 {select.values[0]}", ephemeral=True)
        if select.values[0] == "maybe":
            await interaction.response.send_message(f"You picked2 {select.values[0]}", ephemeral=True)
