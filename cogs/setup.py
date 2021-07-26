from discord.ext import commands
import discord
import datetime
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption)
import json

with open("./setup.json", "r") as f:
    data = json.load(f)


class Cogs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def settings(self, message):
        if not str(message.guild.id) in data:
            if message.author.guild_permissions.administrator:
                def new_guild():
                    data[str(message.guild.id)] = {}
                    data[str(message.guild.id)]["logger"] = {}
                    data[str(message.guild.id)]["logger"]["status"] = "disable"
                    data[str(message.guild.id)]["logger"]["channelid"] = "None"
                    data[str(message.guild.id)]["audit"] = {}
                    data[str(message.guild.id)]["audit"]["status"] = "disable"
                    data[str(message.guild.id)]["audit"]["channelid"] = "None"
                    data[str(message.guild.id)]["invite"] = {}
                    data[str(message.guild.id)]["invite"]["status"] = "disable"
                    data[str(message.guild.id)]["invite"]["role1"] = "None"
                    data[str(message.guild.id)]["language"] = "english"
                    data[str(message.guild.id)]["team role"] = "None"

                    with open("./setup.json", "w")as file:
                        json.dump(data, file)
                    return

                new_guild()
        if str(message.guild.id) in data:
            language = data[str(message.guild.id)]["language"]
            if language == "german":
                if message.author.guild_permissions.administrator:
                    audit_status = data[str(message.guild.id)]["audit"]["status"]
                    audit_channel = data[str(message.guild.id)]["audit"]["channelid"]
                    logger_status = data[str(message.guild.id)]["logger"]["status"]
                    logger_channel = data[str(message.guild.id)]["logger"]["channelid"]
                    invite_status = data[str(message.guild.id)]["invite"]["status"]
                    invite_role = data[str(message.guild.id)]["invite"]["role1"]
                    team_role = data[str(message.guild.id)]["team role"]
                    embed = discord.Embed(title="Settings",
                                            description=f"Wenn du etwas ändern willst gebe den Command `edit` ein")
                    embed.add_field(name="Language", value=f"```{language}```", inline=True)
                    embed.add_field(name="Audit Logger",
                                        value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                    embed.add_field(name="Message Logger",
                                        value=f"```{logger_status}``` **Channel:** <#{logger_channel}>", inline=True)
                    embed.add_field(name="Invite Deleter",
                                        value=f"```{invite_status}``` **Role:** <@&{invite_role}>", inline=True)
                    embed.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text=f"Settings von {message.guild.name}", icon_url=message.guild.icon_url)
                    m = await message.send(embed=embed)
                    channel = message.channel

                    def check1(m):
                        return m.channel == channel and m.content and m.author == message.author

                    msg = await self.client.wait_for('message', check=check1, timeout=120.00)
                    if message.author.id == msg.author.id:
                        if msg.content == "edit":
                            embed2 = discord.Embed(title="Settings")
                            embed2.add_field(name="Language", value=f"```{language}```", inline=True)
                            embed2.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                            embed2.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                            embed2.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                            embed2.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                            embed2.timestamp = datetime.datetime.now()
                            embed2.set_footer(text=f"Settings von {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                            await channel.purge(limit=1)
                            await m.edit(embed=embed2, components=[Select(placeholder="Was willst du bearbeiten?",
                                                                              options=[SelectOption(label="Sprache",
                                                                                                    value="Wähle die Sprache"),
                                                                                       SelectOption(
                                                                                           label="Audit Logger",
                                                                                           value="Einstellungen von Audit Logger"),
                                                                                       SelectOption(
                                                                                           label="Message Logger",
                                                                                           value="Einstellungen von Message Logger"),
                                                                                       SelectOption(
                                                                                           label="Invite Deleter",
                                                                                           value="Einstellungen von Invite Deleter"),
                                                                                       SelectOption(label="Team Role",
                                                                                                    value="Role id von der Team Role")])])
                            interaction = await self.client.wait_for("select_option")
                            await channel.purge(limit=2)
                            if interaction.component[0].label == "Sprache":
                                await message.send(embed=embed2, components=[
                                        Select(placeholder="Welche Sprache willst du auswählen?", options=[
                                            SelectOption(label="German", value="Stelle die Sprache auf Deutsch"),
                                            SelectOption(label="English", value="Set the Language to English")])])
                                interaction2 = await self.client.wait_for("select_option")
                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{interaction2.component[0].label}```", inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings von {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                if interaction2.component[0].label == "German":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["language"] = "german"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "English":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["language"] = "english"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                            if interaction.component[0].label == "Message Logger":
                                await message.send(embed=embed, components=[
                                        Select(placeholder="Message Logger Settings", options=[
                                            SelectOption(label="Enable", value="Aktiviert den Message Logger"),
                                            SelectOption(label="Disable", value="Deaktiviert den Message Logger"),
                                            SelectOption(label="Channel",
                                                         value="Wähle aus in welchen Channel die Nachrichten geloggt werden sollen")])])
                                interaction2 = await self.client.wait_for("select_option")
                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{language}```", inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{interaction2.component[0].label}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings von {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                if interaction2.component[0].label == "Enable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["logger"]["stauts"] = "enable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Disable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["logger"]["stauts"] = "disable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Channel":
                                    await channel.purge(limit=1)
                                    await message.send("Bitte schicke die Channel ID hier rein")

                                    def check2(m):
                                        return m.channel == channel and m.content and m.author == message.author

                                    msg2 = await self.client.wait_for('message', check=check1, timeout=120.00)
                                    data[str(message.guild.id)]["logger"]["channelid"] = msg2.content
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    embedend = discord.Embed(title="Settings")
                                    embedend.add_field(name="Language", value=f"```{language}```", inline=True)
                                    embedend.add_field(name="Audit Logger",
                                                           value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                           inline=True)
                                    embedend.add_field(name="Message Logger",
                                                           value=f"```{logger_status}``` **Channel:** <#{msg2.content}>",
                                                           inline=True)
                                    embedend.add_field(name="Invite Deleter",
                                                           value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                           inline=True)
                                    embedend.timestamp = datetime.datetime.now()
                                    embedend.set_footer(text=f"Settings von {message.guild.name}",
                                                            icon_url=message.guild.icon_url)
                                    await message.send(embed=embedend)
                            if interaction.component[0].label == "Audit Logger":
                                await message.send(embed=embed, components=[
                                        Select(placeholder="Audit Logger Settings", options=[
                                            SelectOption(label="Enable", value="Aktiviert den Audit Logger"),
                                            SelectOption(label="Disable", value="Deaktiviert den Audit Logger"),
                                            SelectOption(label="Channel",
                                                         value="Wähle aus in welchen Channel der Audit geloggt werden sollen")])])
                                interaction2 = await self.client.wait_for("select_option")
                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{language}```", inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{interaction2.component[0].label}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings von {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                if interaction2.component[0].label == "Enable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["audit"]["stauts"] = "enable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Disable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["audit"]["stauts"] = "disable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Channel":
                                    await channel.purge(limit=1)
                                    await message.send("Bitte schicke die Channel ID hier rein")

                                    def check2(m):
                                        return m.channel == channel and m.content and m.author == message.author

                                    msg2 = await self.client.wait_for('message', check=check1, timeout=120.00)
                                    data[str(message.guild.id)]["audit"]["channelid"] = msg2.content
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    embedend = discord.Embed(title="Settings")
                                    embedend.add_field(name="Language", value=f"```{language}```", inline=True)
                                    embedend.add_field(name="Audit Logger",
                                                           value=f"```{audit_status}``` **Channel:** <#{msg2.content}>",
                                                           inline=True)
                                    embedend.add_field(name="Message Logger",
                                                           value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                           inline=True)
                                    embedend.add_field(name="Invite Deleter",
                                                           value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                           inline=True)
                                    embedend.timestamp = datetime.datetime.now()
                                    embedend.set_footer(text=f"Settings von {message.guild.name}",
                                                            icon_url=message.guild.icon_url)
                                    await message.send(embed=embedend)
                            if interaction.component[0].label == "Invite Deleter":
                                await message.send(embed=embed, components=[
                                        Select(placeholder="Invite Deleter Settings", options=[
                                            SelectOption(label="Enable", value="Aktiviert den Invite Deleter"),
                                            SelectOption(label="Disable", value="Deaktiviert den Invite Deleter"),
                                            SelectOption(label="Ignored Role",
                                                         value="Wähle aus welche Rolle vom  löschen der Invites ignoriert werden soll")])])
                                interaction2 = await self.client.wait_for("select_option")
                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{language}```", inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{interaction2.component[0].label}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings von {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                if interaction2.component[0].label == "Enable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["invite"]["stauts"] = "enable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Disable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["invite"]["stauts"] = "disable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Ignored Role":
                                    await channel.purge(limit=1)
                                    await message.send("Bitte schicke die Role ID hier rein")

                                    def check2(m):
                                        return m.channel == channel and m.content and m.author == message.author

                                    msg2 = await self.client.wait_for('message', check=check2, timeout=120.00)
                                    data[str(message.guild.id)]["invite"]["role1"] = msg2.content
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    embedend = discord.Embed(title="Settings")
                                    embedend.add_field(name="Language", value=f"```{language}```", inline=True)
                                    embedend.add_field(name="Audit Logger",
                                                           value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                           inline=True)
                                    embedend.add_field(name="Message Logger",
                                                           value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                           inline=True)
                                    embedend.add_field(name="Invite Deleter",
                                                           value=f"```{invite_status}``` **Role:** <@&{msg2.content}>",
                                                           inline=True)
                                    embedend.timestamp = datetime.datetime.now()
                                    embedend.set_footer(text=f"Settings von {message.guild.name}",
                                                            icon_url=message.guild.icon_url)
                                    await message.send(embed=embedend)
                            if interaction.component[0].label == "Team Role":
                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2, timeout=120.00)

                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{language}```",
                                                 inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{msg2.content}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings von {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                await message.send("Bitte schicke die Role id hier in den Chat")
                                data[str(message.guild.id)]["team role"] = msg2.content
                                with open("./setup.json", "w") as file:
                                    json.dump(data, file)
                                await message.send(embed=embed3)

                if not message.author.guild_permissions.administrator:
                    await message.send("Du hast nicht genug Berechtigungen für diesen Command\n"
                                           "```Benötigte Berechtigungen = Adminstator```")

            if language == "english":
                if message.author.guild_permissions.administrator:
                    team_role = data[str(message.guild.id)]["team role"]
                    audit_status = data[str(message.guild.id)]["audit"]["status"]
                    audit_channel = data[str(message.guild.id)]["audit"]["channelid"]
                    logger_status = data[str(message.guild.id)]["logger"]["status"]
                    logger_channel = data[str(message.guild.id)]["logger"]["channelid"]
                    invite_status = data[str(message.guild.id)]["invite"]["status"]
                    invite_role = data[str(message.guild.id)]["invite"]["role1"]
                    embed = discord.Embed(title="Settings",
                                              description=f"If you want to change something use `edit`")
                    embed.add_field(name="Language", value=f"```{language}```", inline=True)
                    embed.add_field(name="Audit Logger",
                                        value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                        inline=True)
                    embed.add_field(name="Message Logger",
                                        value=f"```{logger_status}``` **Channel:** <#{logger_channel}>", inline=True)
                    embed.add_field(name="Invite Deleter",
                                        value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                        inline=True)
                    embed.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text=f"Settings of {message.guild.name}", icon_url=message.guild.icon_url)
                    m = await message.send(embed=embed)
                    channel = message.channel

                    def check1(m):
                        return m.channel == channel and m.content and m.author == message.author

                    msg = await self.client.wait_for('message', check=check1, timeout=120.00)
                    if message.author.id == msg.author.id:
                        if msg.content == "edit":
                            embed2 = discord.Embed(title="Settings")
                            embed2.add_field(name="Language", value=f"```{language}```", inline=True)
                            embed2.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                            embed2.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                            embed2.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                            embed2.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                            embed2.timestamp = datetime.datetime.now()
                            embed2.set_footer(text=f"Settings of {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                            await channel.purge(limit=1)
                            await m.edit(embed=embed2, components=[Select(placeholder="What do you want to edit?",
                                                                              options=[SelectOption(label="Language",
                                                                                                    value="Select the Bots Language"),
                                                                                       SelectOption(
                                                                                           label="Audit Logger",
                                                                                           value="Settings of Audit Logger"),
                                                                                       SelectOption(
                                                                                           label="Message Logger",
                                                                                           value="Settings of Message Logger"),
                                                                                       SelectOption(
                                                                                           label="Invite Deleter",
                                                                                           value="Settings of Invite Deleter"),
                                                                                       SelectOption(label="Team Role", value="Role id of the Team role")])])
                            interaction = await self.client.wait_for("select_option")
                            await channel.purge(limit=2)
                            if interaction.component[0].label == "Language":
                                await message.send(embed=embed2, components=[
                                    Select(placeholder="What Language do you want?", options=[
                                        SelectOption(label="German", value="Set Language to German"),
                                            SelectOption(label="English", value="Set Language to English")])])
                                interaction2 = await self.client.wait_for("select_option")
                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{interaction2.component[0].label}```", inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings of {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                if interaction2.component[0].label == "German":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["language"] = "german"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "English":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["language"] = "english"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                            if interaction.component[0].label == "Message Logger":
                                await message.send(embed=embed, components=[
                                        Select(placeholder="Message Logger Settings",
                                               options=[
                                                   SelectOption(label="Enable", value="Activate the Message Logger"),
                                                   SelectOption(label="Disable",
                                                                value="Deaktivate the Message Logger"),
                                                   SelectOption(label="Channel",
                                                                value="Select where the Message get Logged")])])
                                interaction2 = await self.client.wait_for("select_option")
                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{language}```", inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{interaction2.component[0].label}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings of {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                if interaction2.component[0].label == "Enable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["logger"]["stauts"] = "enable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Disable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["logger"]["stauts"] = "disable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Channel":
                                    await channel.purge(limit=1)
                                    await message.send("Pls enter the Channel ID")

                                    def check2(m):
                                        return m.channel == channel and m.content and m.author == message.author

                                    msg2 = await self.client.wait_for('message', check=check2, timeout=120.00)
                                    data[str(message.guild.id)]["logger"]["channelid"] = msg2.content
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    embedend = discord.Embed(title="Settings")
                                    embedend.add_field(name="Language", value=f"```{language}```", inline=True)
                                    embedend.add_field(name="Audit Logger",
                                                           value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                           inline=True)
                                    embedend.add_field(name="Message Logger",
                                                           value=f"```{logger_status}``` **Channel:** <#{msg2.content}>",
                                                           inline=True)
                                    embedend.add_field(name="Invite Deleter",
                                                           value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                           inline=True)
                                    embedend.timestamp = datetime.datetime.now()
                                    embedend.set_footer(text=f"Settings of {message.guild.name}",
                                                            icon_url=message.guild.icon_url)
                                    await message.send(embed=embedend)
                            if interaction.component[0].label == "Audit Logger":
                                await message.send(embed=embed,
                                                       components=[Select(placeholder="Audit Logger Settings",
                                                                          options=[SelectOption(label="Enable",
                                                                                                value="Activate the Audit Logger"),
                                                                                   SelectOption(
                                                                                       label="Disable",
                                                                                       value="Deactivate the Audit Logger"),
                                                                                   SelectOption(
                                                                                       label="Channel",
                                                                                       value="Select where the Audit get logged")])])
                                interaction2 = await self.client.wait_for("select_option")
                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{language}```", inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{interaction2.component[0].label}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings of {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                if interaction2.component[0].label == "Enable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["audit"]["stauts"] = "enable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Disable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["audit"]["stauts"] = "disable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Channel":
                                    await channel.purge(limit=1)
                                    await message.send("Pls enter the Channel ID")

                                    def check2(m):
                                        return m.channel == channel and m.content and m.author == message.author

                                    msg2 = await self.client.wait_for('message', check=check2, timeout=120.00)
                                    data[str(message.guild.id)]["audit"]["channelid"] = msg2.content
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    embedend = discord.Embed(title="Settings")
                                    embedend.add_field(name="Language", value=f"```{language}```", inline=True)
                                    embedend.add_field(name="Audit Logger",
                                                           value=f"```{audit_status}``` **Channel:** <#{msg2.content}>",
                                                           inline=True)
                                    embedend.add_field(name="Message Logger",
                                                           value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                           inline=True)
                                    embedend.add_field(name="Invite Deleter",
                                                           value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                           inline=True)
                                    embedend.timestamp = datetime.datetime.now()
                                    embedend.set_footer(text=f"Settings of {message.guild.name}",
                                                            icon_url=message.guild.icon_url)
                                    await message.send(embed=embedend)
                            if interaction.component[0].label == "Invite Deleter":
                                await message.send(embed=embed, components=[
                                        Select(placeholder="Invite Deleter Settings",
                                               options=[
                                                   SelectOption(label="Enable", value="Activate the Invite Deleter"),
                                                   SelectOption(label="Disable",
                                                                value="Deactivate the Invite Deleter"),
                                                   SelectOption(label="Ignored Role",
                                                                value="Select the Role who can send Links")])])
                                interaction2 = await self.client.wait_for("select_option")
                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{language}```", inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{interaction2.component[0].label}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{team_role}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings of {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                if interaction2.component[0].label == "Enable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["invite"]["stauts"] = "enable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Disable":
                                    await channel.purge(limit=1)
                                    data[str(message.guild.id)]["invite"]["stauts"] = "disable"
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    await message.send(embed=embed3)
                                if interaction2.component[0].label == "Ignored Role":
                                    await channel.purge(limit=1)
                                    await message.send("Pls enter the Role ID")

                                    def check2(m):
                                        return m.channel == channel and m.content and m.author == message.author

                                    msg2 = await self.client.wait_for('message', check=check2, timeout=120.00)
                                    data[str(message.guild.id)]["invite"]["role1"] = msg2.content
                                    with open("./setup.json", "w") as file:
                                        json.dump(data, file)
                                    embedend = discord.Embed(title="Settings")
                                    embedend.add_field(name="Language", value=f"```{language}```", inline=True)
                                    embedend.add_field(name="Audit Logger",
                                                           value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                           inline=True)
                                    embedend.add_field(name="Message Logger",
                                                           value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                           inline=True)
                                    embedend.add_field(name="Invite Deleter",
                                                           value=f"```{invite_status}``` **Role:** <@&{msg2.content}>",
                                                           inline=True)
                                    embedend.timestamp = datetime.datetime.now()
                                    embedend.set_footer(text=f"Settings of {message.guild.name}",
                                                            icon_url=message.guild.icon_url)
                                    await message.send(embed=embedend)
                            if interaction.component[0].label == "Team Role":
                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author
                                msg2 = await self.client.wait_for('message', check=check2, timeout=120.00)

                                embed3 = discord.Embed(title="Settings")
                                embed3.add_field(name="Language", value=f"```{language}```",
                                                 inline=True)
                                embed3.add_field(name="Audit Logger",
                                                 value=f"```{audit_status}``` **Channel:** <#{audit_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Message Logger",
                                                 value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                                 inline=True)
                                embed3.add_field(name="Invite Deleter",
                                                 value=f"```{invite_status}``` **Role:** <@&{invite_role}>",
                                                 inline=True)
                                embed3.add_field(name="Team role", value=f"```<@&{msg2.content}>```", inline=True)
                                embed3.timestamp = datetime.datetime.now()
                                embed3.set_footer(text=f"Settings of {message.guild.name}",
                                                  icon_url=message.guild.icon_url)
                                await message.send("Pls enter the Role ID of the Server Team Role")
                                data[str(message.guild.id)]["team role"] = msg2.content
                                with open("./setup.json", "w") as file:
                                    json.dump(data, file)
                                await message.send(embed=embed3)

                    if not message.author.guild_permissions.administrator:
                        await message.send("You dont't have enough Permissions to do this command\n"
                                           "```Required Permissions: Adminstator```")


def setup(client):
      client.add_cog(Cogs(client))
