import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os

from itertools import chain

class user_statsMenu(discord.ui.Select):
    def __init__(self, interaction):
        super().__init__(placeholder="Wähle einen Nutzer aus")
        members = interaction.guild.members

        for member in members:
            self.add_option(label=str(member))

    async def callback(self, interaction: discord.Interaction):

        user_stats_embed = discord.Embed()
        user_stats_embed.color = discord.Color.gold()
        user_stats_embed.set_footer(text=f"requested by: {interaction.user.name}")

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB"),
            port=os.getenv("DB.PORT")
        )

        for member in self.values:

            select_member = mydb.cursor()

            select_member_sql = "SELECT iddiscord_user FROM discord_user WHERE username = %s"
            select_member.execute(select_member_sql, (member.split("#", 1)[0],))

            select_member_result = select_member.fetchall()

            for res in select_member_result:

                select_student_name = mydb.cursor()

                select_student_name_sql = "SELECT first_name, last_name FROM student s \
                JOIN discord_user d ON s.discord_user_iddiscord_user = d.iddiscord_user WHERE d.iddiscord_user = %s"
                select_student_name.execute(select_student_name_sql, (str(res).strip("(',')"),))

                select_student_name_result = select_student_name.fetchall()

                student_name = list(chain(*select_student_name_result))

                user_stats_embed.title = str(f"{student_name[0]} {student_name[1]}")

        await interaction.response.send_message(embed=user_stats_embed)


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