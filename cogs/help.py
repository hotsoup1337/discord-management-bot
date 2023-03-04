import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

class PageButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode, bot):
        super().__init__(label=text, style=buttonStyle)
        self.mode = mode
        self.bot = bot
    
    async def callback(self, interaction: discord.Interaction):

        await interaction.respone.defer()

        if self.mode == 1: 
            await interaction.message.edit()


class HelpView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(PageButton("Vorwärts", discord.ButtonStyle.primary, 0, bot))
        self.add_item(PageButton("Rückwärts", discord.ButtonStyle.primary, 1, bot))

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Zeigt die Hilfe an", aliases=["hilfe"])
    @app_commands.checks.has_role("MET 11")
    async def help(self, bot, interaction: discord.Interaction, member: discord.Member=None):

        helpInfoCard = discord.Embed(title="Hilfe-Panel")
        helpInfoCard.color = discord.Color.blurple()
        helpInfoCard.description = "Hilfe für jegliche Befehle, einfach blättern."
        helpInfoCard.set_author(name=bot.user.name, icon_url=bot.display_avatar.url)

        helpInfoCard.add_field(
            name="Note Eintragen",
            value="Hier findest du Hilfe, um deine Note vernünftig einzutragen!",
            inline=False
        )

        await interaction.response.send_message(embed=helpInfoCard)

async def setup(bot):
    await bot.add_cog(help(bot))