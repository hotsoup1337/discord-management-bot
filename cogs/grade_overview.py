import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

class SelectMenuLesson(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Wähle ein Lernfeld aus.", max_values=1, min_values=1)
        # add for loop -> every lesson in database and add an option
        # label = lesson name
        # description = teacher form_of_address + name
        self.add_option(label="Lernfeld Test", description="Herr Mustermann")

        # how to save the selected lesson together with the selected grade?

    async def callback(self, interaction: discord.Interaction):
        # load into the database
        await interaction.respone.send_message("Test")


class SelectionLessonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectMenuLesson())
        #self.add_item()


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

        sql = "SELECT iduser FROM discord_user WHERE iduser=%s"
        val = (str(interaction.user.id))


        mycursor.execute(sql, val)
        interaction.response.send_message("successful")

async def setup(bot):
    await bot.add_cog(grade_overview(bot))