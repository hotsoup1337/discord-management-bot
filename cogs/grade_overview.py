import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

class RegisterMenuButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode):
        super().__init__(label=text, style=buttonStyle)
        self.mode = mode

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if self.mode == 1:
            await interaction.message.edit(content="Prozess abgebrochen!", delete_after=5)

class RegisterMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RegisterMenuButton("Registriere dich hier!", discord.ButtonStyle.primary, 0))
        self.add_item(RegisterMenuButton("Abbrechen", discord.ButtonStyle.red, 1))



class grade_overview(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="note_eintragen", description="Note eintragen")
    @app_commands.checks.has_role("MET 11")
    async def insert_grade(self, interaction: discord.Interaction, lesson: str, grade: int, member: discord.Member=None):

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        mycursor = mydb.cursor()

        sql = "SELECT iddiscord_user FROM discord_user WHERE iddiscord_user = %s"
        val = str(interaction.user.id)

        mycursor.execute(sql, (val,)) # (val,) tuple
        myresult = mycursor.fetchall()
        if not myresult:
            await interaction.response.send_message("Das System konnte dich nicht finden, bist du nicht registriert? \n Wenn du dich registrieren möchtest, dann klicke auf den Button!", view=RegisterMenuView())
        else:
            user_id = str(myresult[0])
            await interaction.response.send_message(user_id[2:20])  # substring the result to the length of the discord user id and send it to the channel




async def setup(bot):
    await bot.add_cog(grade_overview(bot))