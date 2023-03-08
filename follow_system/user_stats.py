import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

class user_statsMenu(discord.ui.Select):
    def __init__(self, interaction):
        super().__init__(placeholder="Wähle einen Nutzer aus")
        members = interaction.guild.members

        for member in members:
            self.add_option(label=str(member))

    async def callback(self, interaction: discord.Interaction):

        mydb = mysql.connector.connect(
            host=os.getenv("DB.USER"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        interaction.response.send_message("test2")

class user_statsView(discord.ui.View):
    def __init__(self, interaction):
        super().__init__(timeout=None)
        self.add_item(user_statsMenu(interaction))

class setup_user_stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="user_stats", description="Statistiken eines Nutzers anzeigen")
    async def user_stats(self, interaction: discord.Interaction):

        await interaction.response.send_message(view=user_statsView(interaction))

async def setup(bot):
    await bot.add_cog(setup_user_stats(bot))