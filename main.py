import datetime
import json

import discord
import pytz
from dateutil import parser
from discord.ext import tasks, commands

import os
from dotenv import load_dotenv
from cogs import messages

import mysql.connector

class Client(commands.Bot):
    load_dotenv("settings.env")

    #def __int__(self, intents):
        #super().__init__(command_prefix="!", intents=intents)      #unwichtig? kann man unten beim run definieren....

    #ban_words = ["Blödmann", "Musterstrasse 12 Frankfurt 069"]

    async def on_ready(self):


        print("Bot is ready to go!")

        mydb = mysql.connector.connect(
            host=os.getenv("DB.HOST"),
            user=os.getenv("DB.USER"),
            password=os.getenv(("DB.PW"))
        )

        print(f"Database connection successfully established.", mydb)

        #with open('banned_members.json', 'r') as banned_member_file:  # umbauen in Datenbank, statt JSON
        #    self.banned_members = json.load(banned_member_file)

        #self.checkBannedUsers.start()

        #await self.checkMessages()

        #await self.add_cog(Messages.Messages(self))
        await self.load_extension("cogs.Messages")
        #await self.checkMessages()
        await self.tree.sync()

        await self.change_presence(status=discord.Status.dnd, activity=discord.Game(" with Documents"))

    async def on_message(self, message):

        if message.author == self.user:
            return

#        await self.checkMessage(message)

        # print("Message recognized.")
        # print(message.content)
        # print(message.author.name)
        # await message.author.send("Hey this is a private message")
        # print out user stats
        if message.content.startswith("!stats"):
            completeText = message.content.split(" ")[
                           1:]  # [1:] indicates the code to start from point 1 in the array [0, 1, 2]
            print(completeText)

            completeName = ""
            for namePart in completeText:  # name from array 1 to ... gets looped and put into namePart
                completeName += namePart  # chain both variables so you get the content without " "

            allMembers = message.guild.members  # list of all guild members
            for member in allMembers:
                if member.name.replace(" ",
                                       "") == completeName:  # replaces member names where " " are available with "" and checks if it fits the mentioned (by text) user
                    await message.channel.send("Here are the stats from: " + member.name,
                                               delete_after=3)  # delete_after in 3s
                    return
                await message.channel.send("User not found", delete_after=3)  # error

        # Delete messages from a specific user
        if message.content.startswith("!delete messages from"):
            completeText = message.content.split(" ")[3:]
            print(completeText)

            completeName = ""
            for namePart in completeText:
                completeName = completeName + " " + namePart
            # print(completeName.strip()) #delete spaces infront and after string

            member = discord.utils.get(message.guild.members, name=completeName.strip())
            allTextChannels = message.guild.text_channels
            for channel in allTextChannels:
                print(channel)

            async for message in channel.history():  # this is used for deleting the messages as well but in every text channel of the guild BE CAREFUL WITH THIS
                if message.author == member:
                    await message.delete()

            # async for message in message.channel.history(limit=20): #messages will be deleted of user in that channel [limit = 20 messages]
            #    if message.author == member:
            #        await message.delete()

        # Delete messages older than the given date
        if message.content.startswith("!delete messages older"):
            timeString = message.content.split(" ")[3:]
            # print (completeText)

            completeDateString = ""
            for date in timeString:
                completeDateString = completeDateString + " " + date
            print(completeDateString.strip())

            inputDate = parser.parse(completeDateString.strip())
            inputDate = pytz.utc.localize(inputDate)
            allTextChannels = message.guild.text_channels
            for channel in allTextChannels:
                async for message in channel.history():
                    if message.created_at < inputDate:
                        await message.delete()

        if message.content.startswith("info"):
            fullName = message.content.split(" ")[1:]
            fullName = "".join(fullName)
            member = discord.utils.get(message.guild.members, name=fullName)

            memberInfoCard = discord.Embed(title=member.name)
            memberInfoCard.color = discord.Color.gold()
            memberInfoCard.set_thumbnail(url=member.display_avatar.url)
            memberInfoCard.description = "Info über User"
            memberInfoCard.set_author(name=message.author.name, url="https://www.hotsoup1337.com",
                                      icon_url=member.display_avatar.url)
            memberInfoCard.add_field(
                name="ID",
                value=str(member.id),
                inline=False
            )
            memberInfoCard.add_field(
                name="Mitglied seit",
                value=member.joined_at.strftime("%B %d, %Y"),
                inline=True
            )
            memberInfoCard.add_field(
                name="Status",
                value=member.desktop_status,
                inline=True
            )
            memberInfoCard.add_field(
                name="Rollen",
                value=", ".join(role.name for role in member.roles if role.name != "@everyone"),
                inline=False
            )

            memberInfoCard.set_footer(
                text="This message was created by a bot."
            )

            file = discord.File("G:/Downloads/test.jpg", filename="test.jpg")
            memberInfoCard.set_image(url="attachment://test.jpg")

            await message.channel.send(file=file, embed=memberInfoCard)

        await self.process_commands(message)

    # Check messages for ban words
    #async def checkMessages(self):
    #    server = self.get_guild(1078029337091125270)
    #    allTextChannels = server.text_channels
    #    for channel in allTextChannels:
    #        async for message in channel.history():
    #            if message.content in self.ban_words:
    #                await message.delete()

#    async def checkMessage(self, message):
#        if message.content in self.ban_words:
#            await message.delete()

            # wird für 20 sekunden gebannt

#            self.banned_members[message.author.id] = str(datetime.datetime.now() + datetime.timedelta(seconds=20))

#            with open('banned_members.json', 'w') as banned_member_file:
 #               json.dump(self.banned_members, banned_member_file)

 #           await message.author.ban()

    async def on_raw_reaction_add(self, payload):
        # print(payload.guild_id)
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        skull_role = discord.utils.get(channel.guild.roles, name="Skull")
        cry_role = discord.utils.get(channel.guild.roles, name="Cry")

        getRoleChannel = 1079033479611830272
        MessageID = 1079033586453336064

        if channel.id == getRoleChannel and message.id == MessageID:
            if payload.emoji.name == "💀":
                await payload.member.add_roles(skull_role)

        if channel.id == getRoleChannel and message.id == MessageID:
            if payload.emoji.name == "😭":
                await payload.member.add_roles(cry_role)

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        author = discord.utils.get(channel.guild.members, id=payload.user_id)

        skull_role = discord.utils.get(channel.guild.roles, name="Skull")
        cry_role = discord.utils.get(channel.guild.roles, name="Cry")

        getRoleChannel = 1079033479611830272
        MessageID = 1079033586453336064

        if channel.id == getRoleChannel and message.id == MessageID:
            if payload.emoji.name == "💀":
                await author.remove_roles(skull_role)

        if channel.id == getRoleChannel and message.id == MessageID:
            if payload.emoji.name == "😭":
                await author.remove_roles(cry_role)

    async def on_member_join(self, member):
        joinRole = discord.utils.get(member.guild.roles, name="Join")
        await member.add_roles(joinRole)

    @tasks.loop(seconds=5)
    async def checkBannedUsers(self):
        for key, value in self.banned_members.items():
            unban_time = parser.parse(value)
            if unban_time < datetime.datetime.now():
                server = self.get_guild(1078029337091125270)
                user_to_unban = await self.fetch_user(int(key))

                await server.unban(user_to_unban)
                self.banned_members.pop(key)

                with open("banned_members.json", "w") as banned_members_file:
                    json.dump(self.banned_members, banned_members_file)

                return


intents = discord.Intents.all()
client = Client(command_prefix="!", intents=intents)
client.run(os.getenv('TOKEN'))
