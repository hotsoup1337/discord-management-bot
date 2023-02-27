import discord
from discord import app_commands
from discord.ext import commands

import mysql.connector
import os


class MusicButton(discord.ui.Button):
    def __init__(self, text, buttonStyle, mode, bot):
        super().__init__(label=text, style=buttonStyle)
        self.mode = mode
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        #await interaction.response.send_message("Ich wurde angeklickt!")

        await interaction.response.defer()

        voice_channel = discord.utils.get(interaction.guild.voice_channels, name="General")
        #voice_client = await voice_channel.connect()

        voice_client = discord.utils.get(self.bot.voice_clients, channel=voice_channel)
        if voice_client == None:
            voice_client = await voice_channel.connect()

        if self.mode == 0:
            voice_client.play(discord.FFmpegPCMAudio(source="./Music/MusicFile.mp3", executable="ffmpeg.exe"))
        elif self.mode == 1:
            voice_client.pause()
        elif self.mode == 2:
            voice_client.resume()
        elif self.mode == 3:
            voice_client.stop()
            await voice_client.disconnect()

class MusicView(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.add_item(MusicButton("Play Music", discord.ButtonStyle.primary, 0, bot))
        self.add_item(MusicButton("Pause Music", discord.ButtonStyle.secondary, 1, bot))
        self.add_item(MusicButton("Resume Music", discord.ButtonStyle.green, 2, bot))
        self.add_item(MusicButton("Stop Music", discord.ButtonStyle.red, 3, bot))

class SelectMenu(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Wähle ein Auto", max_values=2, min_values=1)
        self.add_option(label="Mazda RX8", description="Enthält einen Wankelmotor")
        self.add_option(label="Mercedes CL500", description="Enthält einen Wankelmotor")
        self.add_option(label="Toyota Supra", description="Enthält einen Wankelmotor")
        self.add_option(label="Nissan GTR R34", description="Enthält einen Wankelmotor")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Sie haben {self.values} ausgewählt")

class ChanelSelectMenu(discord.ui.ChannelSelect):
    def __init__(self):
        super().__init__(placeholder="Wähle einen Textchannel aus.", channel_types=[discord.ChannelType.text], max_values=1)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = await self.values[0].fetch()
        await channel.send("Was geht?")

class SelectionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectMenu())
        self.add_item(ChanelSelectMenu())

class Messages(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #@commands.Cog.listener()
    #async def on_message_edit(self, before, after):
    #    await before.channel.send(f"Before: {before.content}")
    #    await before.channel.send(f"After: {after.content}")

    @commands.command()
    async def test(self, ctx):
        await ctx.reply("Was geht?")

    @app_commands.command(name="delete_messages", description="Delete Messages")
    @app_commands.checks.has_role("Leiter")
    async def deletemessages(self, interaction: discord.Interaction, number: int, member: discord.Member=None):
        delete_counter = 0
        await interaction.response.send_message(str("Wird gemacht!"), ephemeral=True)
        async for message in interaction.channel.history():
            if message.author == member or member == None:
                await message.delete()
                delete_counter += 1
            if delete_counter == number:
                break

    @deletemessages.error
    async def on_deletemessages_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message(str("Dir fehlt die Rolle!"), ephemeral=True)

    @app_commands.command(name="test_insert", description="Test insert to database")
    @app_commands.checks.has_role("Leiter")
    async def testinsert(self, interaction: discord.Interaction, insert_value: str, member: discord.Member=None):

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv("DB.PW"),
            database=os.getenv("DB")
        )

        mycursor = mydb.cursor()

        sql = "INSERT INTO student VALUES(%s, %s, %s)"
        val = ((int("2")), "Benjamin", "Finck")
        mycursor.execute(sql, val)

        mydb.commit()

        await interaction.response.send_message(str(mycursor.rowcount) + " rows inserted")

    @app_commands.command(name="music")
    async def music(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=MusicView(self.bot))

    @app_commands.command(name="selection")
    async def selection(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=SelectionView())

async def setup(bot):
    await bot.add_cog(Messages(bot))