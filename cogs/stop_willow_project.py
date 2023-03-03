import discord 
from discord import app_commands
from discord.ext import commands


class LinkButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode, url):
        super().__init__(label=text, style=buttonStyle, url=url)

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()


class LinkView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(LinkButton("Change.org", discord.ButtonStyle.primary, 0, url="https://chng.it/5WSrNMvsKM"))
        self.add_item(LinkButton("Probleme mit Englisch? Klicke hier!", discord.ButtonStyle.primary, 1, url=None))

    async def callback(self, interaction: discord.Interaction):

        await interaction.response.defer()

class stop_willow_project(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stop-willow", description="Share the petition for stop willow")
    @app_commands.checks.has_role("MET 11")
    async def stop_willow(self, interaction: discord.Interaction):

        InfoCard = discord.Embed(title="STOP THE WILLOW PROJECT")
        InfoCard.color = discord.Color.blue()
        InfoCard.set_thumbnail(url="https://assets.change.org/photos/9/wz/db/MzWzDBcSvRDWZcW-800x450-noPad.jpg?1677633256")
        InfoCard.description = "The Willow Master Development Plan is the largest proposed oil development project on public lands. Willow would emit more climate pollution annually than more than 99.7% of all single point sources in the country. This project would completely encircle the Iñupiat village of Nuiqsut with oil development, increasing the health risks for the community and surrounding environment. While the majority of Iñupiat are in support of this project, there are still many Iñupiat and other Arctic Indigenous people that oppose this project and its consequences. With the concerns of the environment, climate, and Indigenous communities, it is vital that the Willow Project is declined."
        InfoCard.set_footer(text="Klicke den Button an, wenn du unterschreiben möchtest!")

        await interaction.response.send_message(embed=InfoCard, view=LinkView())

async def setup(bot):
    await bot.add_cog(stop_willow_project(bot))
        
    
