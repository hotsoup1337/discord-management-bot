import discord
from discord import app_commands
from discord.ext import commands


class PageButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode, bot):
        super().__init__(label=text, style=buttonStyle)
        self.mode = mode
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):

        await interaction.respone.defer()

class C


class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Embed here")