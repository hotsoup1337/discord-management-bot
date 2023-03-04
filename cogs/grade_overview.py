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

        if self.mode == 0:
            await interaction.message.delete()
            await interaction.response.send_modal(RegisterUserModal())

        if self.mode == 1:
            await interaction.response.defer()
            await interaction.message.edit(content="Prozess abgebrochen!", delete_after=5)

class RegisterMenuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RegisterMenuButton("Registriere dich hier!", discord.ButtonStyle.primary, 0))
        self.add_item(RegisterMenuButton("Abbrechen", discord.ButtonStyle.red, 1))

class RegisterUserModal(discord.ui.Modal):

    def __init__(self):
        super().__init__(title="Registrierungsformular")

    first_name = discord.ui.TextInput(label="Vorname", style=discord.TextStyle.short, placeholder="Bitte Vornamen eintragen..", required=True)
    last_name = discord.ui.TextInput(label="Nachname", style=discord.TextStyle.short, placeholder="Bitte Nachnamen eintragen..", required=True)

    async def on_submit(self, interaction: discord.Interaction):

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        user_discord_insert = mydb.cursor()

        user_discord_insert_sql = "INSERT INTO discord_user VALUES(%s, %s, %s)"
        user_discord_insert_val = (str(interaction.user.id), interaction.user.name, interaction.user.discriminator)
        user_discord_insert.execute(user_discord_insert_sql, user_discord_insert_val)

        mydb.commit()

        user_student_insert = mydb.cursor()

        user_student_insert_sql = "INSERT INTO student VALUES(NULL, %s, %s, %s)"
        user_student_insert_val = (self.first_name.value, self.last_name.value, str(interaction.user.id))
        user_student_insert.execute(user_student_insert_sql, user_student_insert_val)

        mydb.commit()

        await interaction.response.send_message(f'Du wurdest erfolgreich als: "{self.first_name.value} {self.last_name.value}",  registriert!', ephemeral=True)

class SelectLessonMenu(discord.ui.Select):
    def __init__(self, grade: int):
        super().__init__(placeholder="Wähle ein Lernfeld aus", max_values=1, min_values=1)

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        select_teachers = mydb.cursor()

        select_teachers_sql = "SELECT form_of_address, name, lesson_name FROM teacher, lesson WHERE teacher.idteacher = lesson.teacher_idteacher ORDER BY lesson_name"
        select_teachers.execute(select_teachers_sql)

        select_teachers_result = select_teachers.fetchall()

        for a, b, c in select_teachers_result:
            teacher = a + " " + b
            lesson = c
            self.add_option(label=lesson, description=teacher)

    async def callback(self, interaction: discord.Interaction):

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        for a in self.values:

            select_id = mydb.cursor()

            select_id_sql = "SELECT idlesson FROM lesson WHERE lesson_name = %s"
            select_id.execute(select_id_sql, a)

            select_id_result = select_id.fetchall()

            


class SelectLessonView(discord.ui.View):
    def __init__(self, grade: int):
        super().__init__(timeout=None)
        self.add_item(SelectLessonMenu(grade))

class grade_overview(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="note_eintragen", description="Note eintragen")
    @app_commands.checks.has_role("MET 11")
    async def insert_grade(self, interaction: discord.Interaction, note: int):

        if note <= 6:

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
                await interaction.response.send_message(view=SelectLessonView(note))

        else:
            await interaction.response.send_message("Bitte gebe eine richtige Note an.", ephemeral=True, delete_after=3)



async def setup(bot):
    await bot.add_cog(grade_overview(bot))