import discord
from discord import app_commands
from discord.ext import commands










class setup_user_stats(commands.Cog):
    def __init__(self):
        super().__init__(timeout=None)




async def setup(bot):
    await bot.add_cog(setup_user_stats)