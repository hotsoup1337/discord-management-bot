import discord 
from discord import app_commands
from discord.ext import commands


class LinkButton(discord.ui.Button):
    def __init__(self, text, buttonStyle):
        super().__init__(label=text, style=buttonStyle)

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()


class LinkView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(LinkButton("Change.org", discord.ButtonStyle.primary))

class Messages(commands.Cog):

    def __init__(self):
        self.bot = bot

    @app_commands.command(name="stop-willow", description="Share the petition for stop willow")
    @app_commands.checks.has_role("MET 11")
    async def stop_willow(self, interaction: discord.Interaction):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(str("Missing permissions!", ephmeral=True, delete_after=3))

        else:
            await interaction.response.send_message(view=LinkView(self.bot))

async def setup(bot):
    await bot.add_cog(Messages())
        
    
