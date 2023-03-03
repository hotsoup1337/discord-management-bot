import discord 
from discord import app_commands
from discord.ext import commands


class LinkButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, url):
        super().__init__(label=text, style=buttonStyle, url=url)

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()


class LinkView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(LinkButton("Change.org", discord.ButtonStyle.primary, url="https://chng.it/5WSrNMvsKM"))

class stop_willow_project(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stop-willow", description="Share the petition for stop willow")
    @app_commands.checks.has_role("MET 11")
    async def stop_willow(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=LinkView())

async def setup(bot):
    await bot.add_cog(stop_willow_project(bot))
        
    
