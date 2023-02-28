import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os


class SelectMenuLesson():
    def __init__(self):
        super().__init__(placeholder="Wähle ein Lernfeld aus.", max_values=1, min_values=1)
        # add for loop -> every lesson in database and add an option
        # label = lesson name
        # description = teacher form_of_address + name
        self.add_option(label="Lernfeld Test", description="Herr Mustermann")

        # how to save the selected lesson together with the selected grade?