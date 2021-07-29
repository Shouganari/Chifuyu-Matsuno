import asyncio
import datetime

import discord
from discord.ext import commands
from discord_components import (
    Select,
    SelectOption)

from utils.emoji import *
from utils.mongo import guild_settings


class Cogs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await guild_settings.insert_one(
            {"_id": int(guild.id), "settings": {"logger": {"status": "disable", "channelid": "None"},
                                                "audit": {"status": "disable", "channelid": "None"},
                                                "invite": {"status": "disable", "role1": "None", "channelid": "None"},
                                                "language": "english", "team role": "None"}})
        return

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await guild_settings.delete_one({"_id": int(guild.id)})
        return

    @commands.command()
    @commands.guild_only()
    async def settings(self, message):
        settings = await guild_settings.find_one({"_id": int(message.guild.id)})
        language = settings["settings"]["language"]
        audit_status = settings["settings"]["audit"]["status"]
        audit_channel = settings["settings"]["audit"]["channelid"]
        logger_status = settings["settings"]["logger"]["status"]
        logger_channel = settings["settings"]["logger"]["channelid"]
        invite_status = settings["settings"]["invite"]["status"]
        invite_role = settings["settings"]["invite"]["role1"]
        invite_channel = settings["settings"]["invite"]["channelid"]
        team_role = settings["settings"]["team role"]
        team__role = discord.utils.get(message.guild.roles, id=team_role)
        if language == "german":
            if message.author.guild_permissions.administrator:
                embed = discord.Embed(title=f"Settings {secure}",
                                      description=f"Wenn du etwas ändern willst gebe den Command **edit** ein")
                embed.add_field(name=f"Language", value=f"```{language}```", inline=True)
                if team_role == "None":
                    embed.add_field(name=f"Team role {staff}", value=f"```{team__role}```", inline=True)
                if not team_role == "None":
                    embed.add_field(name=f"Team role {staff}", value=f"```{team__role.name}```", inline=True)
                embed.add_field(name=f"\u200B", value="\u200B", inline=True)
                if audit_status == "enable":
                    embed.add_field(name=f"Audit Logger {on}",
                                    value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                if audit_status == "disable":
                    embed.add_field(name=f"Audit Logger {off}",
                                    value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                if logger_status == "enable":
                    embed.add_field(name=f"Message Logger {on}",
                                    value=f"```{logger_status}``` **Channel:** <#{logger_channel}>", inline=True)
                if logger_status == "disable":
                    embed.add_field(name=f"Message Logger {off}",
                                    value=f"```{logger_status}``` **Channel:** <#{logger_channel}>", inline=True)
                embed.add_field(name=f"\u200B", value="\u200B", inline=True)
                if invite_status == "enable":
                    embed.add_field(name=f"Invite Deleter {on}",
                                    value=f"```{invite_status}``` **Role:** <@&{invite_role}>      <#{invite_channel}>",
                                    inline=True)
                if invite_status == "disable":
                    embed.add_field(name=f"Invite Deleter {off}",
                                    value=f"```{invite_status}``` <@&{invite_role}>      <#{invite_channel}>",
                                    inline=True)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"Settings von {message.guild.name}", icon_url=message.guild.icon_url)
                m = await message.send(embed=embed)
                channel = message.channel

                def check1(m):
                    return m.channel == channel and m.content and m.author == message.author

                msg = await self.client.wait_for('message', check=check1)
                if message.author.id == msg.author.id:
                    if msg.content == "edit":
                        embed2 = discord.Embed(title=f"Settings {secure}")
                        embed2.add_field(name=f"Language", value=f"```{language}```", inline=True)
                        if team_role == "None":
                            embed2.add_field(name=f"Team role {staff}", value=f"```{team_role}```", inline=True)
                        if not team_role == "None":
                            embed2.add_field(name=f"Team role {staff}", value=f"```{team__role.name}```", inline=True)
                        embed2.add_field(name=f"\u200B", value="\u200B", inline=True)
                        if audit_status == "enable":
                            embed2.add_field(name=f"Audit Logger {on}",
                                            value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                        if audit_status == "disable":
                            embed2.add_field(name=f"Audit Logger {off}",
                                            value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                        if logger_status == "enable":
                            embed2.add_field(name=f"Message Logger {on}",
                                            value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                            inline=True)
                        if logger_status == "disable":
                            embed2.add_field(name=f"Message Logger {off}",
                                            value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                            inline=True)
                        embed2.add_field(name=f"\u200B", value="\u200B", inline=True)
                        if invite_status == "enable":
                            embed2.add_field(name=f"Invite Deleter {on}",
                                            value=f"```{invite_status}``` **Role:** <@&{invite_role}>      <#{invite_channel}>",
                                            inline=True)
                        if invite_status == "disable":
                            embed2.add_field(name=f"Invite Deleter {off}",
                                            value=f"```{invite_status}``` **Role:** <@&{invite_role}>      <#{invite_channel}>",
                                            inline=True)
                        embed.timestamp = datetime.datetime.now()
                        embed.set_footer(text=f"Settings von {message.guild.name}", icon_url=message.guild.icon_url)

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
                            if interaction2.component[0].label == "German":
                                settings["settings"]["language"] = "german"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "English":
                                settings["settings"]["language"] = "english"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                        if interaction.component[0].label == "Message Logger":
                            await message.send(embed=embed, components=[
                                Select(placeholder="Message Logger Settings", options=[
                                    SelectOption(label="Enable", value="Aktiviert den Message Logger"),
                                    SelectOption(label="Disable", value="Deaktiviert den Message Logger"),
                                    SelectOption(label="Channel",
                                                 value="Wähle aus in welchen Channel die Nachrichten geloggt werden sollen")])])
                            interaction2 = await self.client.wait_for("select_option")
                            if interaction2.component[0].label == "Enable":
                                settings["settings"]["logger"]["status"] = "enable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Disable":
                                settings["settings"]["logger"]["status"] = "disable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Channel":
                                await message.send("Bitte schicke die Channel ID hier rein")

                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2)
                                channel = self.client.get_channel(int(msg2.content))
                                if channel is not None:
                                    settings["settings"]["logger"]["channelid"] = int(msg2.content)
                                    await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                    await message.send(f"Der Channel wurde auf <#{msg2.content}>")
                                if channel is None:
                                    await message.send(f"Diesen Channel gibt es nicht")
                                await asyncio.sleep(10)
                        if interaction.component[0].label == "Audit Logger":
                            await message.send(embed=embed, components=[
                                Select(placeholder="Audit Logger Settings", options=[
                                    SelectOption(label="Enable", value="Aktiviert den Audit Logger"),
                                    SelectOption(label="Disable", value="Deaktiviert den Audit Logger"),
                                    SelectOption(label="Channel",
                                                 value="Wähle aus in welchen Channel der Audit geloggt werden sollen")])])
                            interaction2 = await self.client.wait_for("select_option")
                            if interaction2.component[0].label == "Enable":
                                settings["settings"]["audit"]["status"] = "enable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Disable":
                                settings["settings"]["logger"]["status"] = "disable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Channel":
                                await message.send("Bitte schicke die Channel ID hier rein")

                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2)
                                channel = self.client.get_channel(int(msg2.content))
                                if channel is not None:
                                    settings["settings"]["audit"]["channelid"] = int(msg2.content)
                                    await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                    await message.send(f"Der Channel wurde auf <#{msg2.content}> gesetzt")

                                if channel is None:
                                    await message.send(f"Diesen Channel gibt es nicht")
                                await asyncio.sleep(10)
                        if interaction.component[0].label == "Invite Deleter":
                            await message.send(embed=embed, components=[
                                Select(placeholder="Invite Deleter Settings", options=[
                                    SelectOption(label="Enable", value="Aktiviert den Invite Deleter"),
                                    SelectOption(label="Disable", value="Deaktiviert den Invite Deleter"),
                                    SelectOption(label="Report Channel",
                                                 value="Der Channel in den die Person die eigenwerbung macht gereportet wird"),
                                    SelectOption(label="Ignored Role",
                                                 value="Wähle aus welche Rolle vom  löschen der Invites ignoriert werden soll")])])
                            interaction2 = await self.client.wait_for("select_option")
                            if interaction2.component[0].label == "Enable":
                                settings["settings"]["invite"]["status"] = "enable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Disable":
                                settings["settings"]["invite"]["status"] = "disable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Ignored Role":
                                await message.send("Bitte schicke die Role ID hier rein")

                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2)
                                role = discord.utils.get(message.guild.roles, id=int(msg2.content))
                                if role is not None:
                                    settings["settings"]["invite"]["role1"] = msg2.content
                                    await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                    await message.send(f"Die Rolle wurde auf <@&{msg2.content}>")
                                if role is None:
                                    await message.send(f"Diese Rolle gibt es nicht")
                                await asyncio.sleep(10)
                            if interaction2.component[0].label == "Report Channel":
                                await message.send("Bitte schicke die Channel ID hier rein")

                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2)

                                settings["settings"]["invite"]["channelid"] = msg2.content
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                await message.send(f"Der Channel wurde auf <#{msg2.content}>")
                                await asyncio.sleep(10)
                        if interaction.component[0].label == "Team Role":
                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                await message.send("Bitte schicke die Role id hier in den Chat")
                                msg2 = await self.client.wait_for('message', check=check2)
                                role = discord.utils.get(message.guild.roles, id=int(msg2.content))
                                if role is not None:
                                    settings["settings"]["team role"] = int(msg2.content)
                                    await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                    await message.send(f"Die Team role ist jetzt <@&{msg2.content}>")
                                if role is None:
                                    await message.send(f"Diesen Channel gibt es nicht")
                                await asyncio.sleep(10)

                        await message.channel.purge(limit=1)
                        await message.reinvoke(restart=True)

            if not message.author.guild_permissions.administrator:
                await message.send("Du hast nicht genug Berechtigungen für diesen Command\n"
                                   "```Benötigte Berechtigungen = Administrator```")

        if language == "english":
            if message.author.guild_permissions.administrator:
                embed = discord.Embed(title=f"Settings {secure}",
                                      description=f"If you want to change something use **edit**")
                embed.add_field(name=f"Language", value=f"```{language}```", inline=True)
                if team_role == "None":
                    embed.add_field(name=f"Team role {staff}", value=f"```{team_role}```", inline=True)
                if not team_role == "None":
                    embed.add_field(name=f"Team role {staff}", value=f"```<{team__role.name}>```", inline=True)
                embed.add_field(name=f"\u200B", value="\u200B", inline=True)
                if audit_status == "enable":
                    embed.add_field(name=f"Audit Logger {on}",
                                    value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                if audit_status == "disable":
                    embed.add_field(name=f"Audit Logger {off}",
                                    value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                if logger_status == "enable":
                    embed.add_field(name=f"Message Logger {on}",
                                    value=f"```{logger_status}``` **Channel:** <#{logger_channel}>", inline=True)
                if logger_status == "disable":
                    embed.add_field(name=f"Message Logger {off}",
                                    value=f"```{logger_status}``` **Channel:** <#{logger_channel}>", inline=True)
                embed.add_field(name=f"\u200B", value="\u200B", inline=True)
                if invite_status == "enable":
                    embed.add_field(name=f"Invite Deleter {on}",
                                    value=f"```{invite_status}``` **Role:** <@&{invite_role}>      <#{invite_channel}>",
                                    inline=True)
                if invite_status == "disable":
                    embed.add_field(name=f"Invite Deleter {off}",
                                    value=f"```{invite_status}``` **Role:** <@&{invite_role}>      <#{invite_channel}>",
                                    inline=True)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"Settings of {message.guild.name}", icon_url=message.guild.icon_url)
                m = await message.send(embed=embed)
                channel = message.channel

                def check1(m):
                    return m.channel == channel and m.content and m.author == message.author

                msg = await self.client.wait_for('message', check=check1)
                if message.author.id == msg.author.id:
                    if msg.content == "edit":
                        embed2 = discord.Embed(title=f"Settings {secure}")
                        embed2.add_field(name=f"Language", value=f"```{language}```", inline=True)
                        if team_role == "None":
                            embed2.add_field(name=f"Team role {staff}", value=f"```{team_role}```", inline=True)
                        if not team_role == "None":
                            embed2.add_field(name=f"Team role {staff}", value=f"```{team__role.name}```", inline=True)
                        embed2.add_field(name=f"\u200B", value="\u200B", inline=True)
                        if audit_status == "enable":
                            embed2.add_field(name=f"Audit Logger {on}",
                                             value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                        if audit_status == "disable":
                            embed2.add_field(name=f"Audit Logger {off}",
                                             value=f"```{audit_status}``` **Channel:** <#{audit_channel}>", inline=True)
                        if logger_status == "enable":
                            embed2.add_field(name=f"Message Logger {on}",
                                             value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                             inline=True)
                        if logger_status == "disable":
                            embed2.add_field(name=f"Message Logger {off}",
                                             value=f"```{logger_status}``` **Channel:** <#{logger_channel}>",
                                             inline=True)
                        embed2.add_field(name=f"\u200B", value="\u200B", inline=True)
                        if invite_status == "enable":
                            embed2.add_field(name=f"Invite Deleter {on}",
                                             value=f"```{invite_status}``` **Role:** <@&{invite_role}>      <#{invite_channel}>",
                                             inline=True)
                        if invite_status == "disable":
                            embed2.add_field(name=f"Invite Deleter {off}",
                                             value=f"```{invite_status}``` **Role:** <@&{invite_role}>      <#{invite_channel}>",
                                             inline=True)
                        embed.timestamp = datetime.datetime.now()
                        embed.set_footer(text=f"Settings of {message.guild.name}", icon_url=message.guild.icon_url)
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
                                                                               SelectOption(label="Team Role",
                                                                                            value="Role id of the Team role")])])
                        interaction = await self.client.wait_for("select_option")
                        await channel.purge(limit=2)
                        if interaction.component[0].label == "Language":
                            await message.send(embed=embed2, components=[
                                Select(placeholder="What Language do you want?", options=[
                                    SelectOption(label="German", value="Set Language to German"),
                                    SelectOption(label="English", value="Set Language to English")])])
                            interaction2 = await self.client.wait_for("select_option")
                            if interaction2.component[0].label == "German":
                                settings["settings"]["language"] = "german"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "English":
                                settings["settings"]["language"] = "english"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
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
                            if interaction2.component[0].label == "Enable":
                                settings["settings"]["logger"]["status"] = "enable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Disable":
                                settings["settings"]["logger"]["status"] = "disable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Channel":
                                await message.send("Pls enter the Channel ID")

                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2)
                                channel = self.client.get_channel(int(msg2.content))
                                if channel is not None:
                                    settings["settings"]["logger"]["channelid"] = int(msg2.content)
                                    await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                    await message.send(f"The Logger Channel got Set to <#{msg2.content}>")
                                if channel is None:
                                    await message.send("This Channel doesn't exist")
                                await asyncio.sleep(10)
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
                            if interaction2.component[0].label == "Enable":
                                settings["settings"]["audit"]["status"] = "enable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Disable":
                                settings["settings"]["audit"]["status"] = "disable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Channel":
                                await message.send("Pls enter the Channel ID")

                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2)
                                channel = self.client.get_channel(int(msg2.content))
                                if channel is not None:
                                    settings["settings"]["audit"]["channelid"] = int(msg2.content)
                                    await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                    await message.send(f"The Channel got set to <#{msg2.content}>")
                                if channel is None:
                                    await message.send("This Channel doesnt exist")
                                await asyncio.sleep(10)
                        if interaction.component[0].label == "Invite Deleter":
                            await message.send(embed=embed, components=[
                                Select(placeholder="Invite Deleter Settings",
                                       options=[
                                           SelectOption(label="Enable", value="Activate the Invite Deleter"),
                                           SelectOption(label="Disable",
                                                        value="Deactivate the Invite Deleter"),
                                           SelectOption(label="Ignored Role",
                                                        value="Select the Role who can send Links"),
                                            SelectOption(label="Report Channel", value="The Channel the people who send the links get reportet")])])
                            interaction2 = await self.client.wait_for("select_option")
                            if interaction2.component[0].label == "Enable":
                                settings["settings"]["invite"]["status"] = "enable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                await message.send(embed=embed2)
                            if interaction2.component[0].label == "Disable":
                                await channel.purge(limit=1)
                                settings["settings"]["invite"]["status"] = "disable"
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                            if interaction2.component[0].label == "Ignored Role":
                                await message.send("Pls enter the Role ID")

                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2)
                                role = discord.utils.get(message.guild.roles, id=int(msg2.content))
                                if role is not None:
                                    settings["settings"]["invite"]["role1"] = int(msg2.content)
                                    await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                    await message.send(f"The Ignored Role got set to <@&{int(msg2.content)}>")
                                if role is None:
                                    await message.send(f"This role doesn't exist")
                                await asyncio.sleep(10)
                            if interaction2.component[0].label == "Report Channel":
                                await message.send("Pls enter the Channel ID")

                                def check2(m):
                                    return m.channel == channel and m.content and m.author == message.author

                                msg2 = await self.client.wait_for('message', check=check2, timeout=120.00)
                                channel = self.client.get_channel(int(msg2.channel))
                                if channel is not None:
                                    await guild_settings.update_one({"_id": int(message.guild.id)},
                                                                    {'$set': settings})
                                    await message.send(f"The Channel got set to <#{msg2.content}>")
                                if channel is None:
                                    await message.send("This Channel doesn't exist")
                                await asyncio.sleep(10)
                        if interaction.component[0].label == "Team Role":
                            def check2(m):
                                return m.channel == channel and m.content and m.author == message.author

                            await message.send("Pls enter the Role ID of the Server Team Role")
                            msg2 = await self.client.wait_for('message', check=check2)
                            role = discord.utils.get(message.guild.roles, id=int(msg2.content))
                            if role is not None:
                                settings["settings"]["team role"] = msg2.content
                                await guild_settings.update_one({"_id": int(message.guild.id)}, {'$set': settings})
                                await message.send(f"The Team role got set to <@&{msg2.content}>")
                            if role is None:
                                await message.send(f"This role doesn't exist")
                            await asyncio.sleep(10)

                        await message.channel.purge(limit=1)
                        await message.reinvoke(restart=True)
            if not message.author.guild_permissions.administrator:
                await message.send("You dont't have enough Permissions to do this command\n"
                                   "```Required Permissions: Administrator```")


def setup(client):
    client.add_cog(Cogs(client))
