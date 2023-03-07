import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector


class user_statsMenu(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Wähle einen Nutzer aus", max_values=1, min_values=1)

        mydb = mysql.connector.connect(

        )



class user_statsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item()

class setup_user_stats(commands.Cog):
    def __init__(self):
        super().__init__(timeout=None)




async def setup(bot):
    await bot.add_cog(setup_user_stats)