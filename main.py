import discord
from discord.ext import tasks, commands

import os
from dotenv import load_dotenv

import mysql.connector

class Client(commands.Bot):
    load_dotenv("settings.env")

    async def on_ready(self):

        print("Bot is ready to go!")

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB"),
            port=os.getenv("DB.PORT")
        )

        await self.load_extension("cogs.messages")
        await self.load_extension("cogs.grade_overview")
        await self.load_extension("cogs.stop_willow_project")
        await self.load_extension("follow_system.user_stats")
        await self.tree.sync()

        await self.change_presence(status=discord.Status.dnd, activity=discord.Game(" with Documents"))

    async def on_message(self, message):

        if message.author == self.user:
            return

intents = discord.Intents.all()
client = Client(command_prefix="!", intents=intents)
client.run(os.getenv('TOKEN'))
