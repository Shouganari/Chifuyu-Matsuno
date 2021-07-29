import asyncio
import datetime
import json
import os
import random

import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle

from utils.mongo import guild_settings

with open("config.json", "r") as f:
    config = json.load(f)

Token = config["Token"]
intents = discord.Intents.all()
client = commands.Bot(command_prefix="ch!", intents=intents, status=discord.Status.online)
client.remove_command("help")


@client.event
async def on_ready():
    DiscordComponents(client)
    print("Bot on")
    presence = ["ch!", "ch!help", "Owner Yuutokata"]
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(presence)))
    await asyncio.sleep(60)


@client.group(invoke_command=True)
async def help(message):
    if message.guild is None:
        delete = [[Button(style=ButtonStyle.red, label="🗑")]]
        button = [
            [Button(style=ButtonStyle.blue, label="Commands"), Button(style=ButtonStyle.blue, label="Admin Commands"),
             Button(style=ButtonStyle.blue, label="Features")],
            Button(style=ButtonStyle.red, label="🗑")]
        prefix = client.command_prefix
        embed = discord.Embed(title="Help", description="For what do you need Help?")
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Shouganari ©")
        await message.send(embed=embed, components=button)
        res = await client.wait_for('button_click')
        if res.component.label == "Commands":
            embed = discord.Embed(title="Help")
            embed.add_field(name="Commands:", value=f"**{prefix}help**\n"
                                                    f"Shows this Command\n\r"
                                                    f"**{prefix}about**\n"
                                                    f"Shows Informations about the Bot\n\r"
                                                    f"**{prefix}code**\n"
                                                    f"You can see the Source Code of Bot\n\r"
                                                    f"**{prefix}dev**\n"
                                                    f"Shows Informations about the Bot Owner/Developer\n\r"
                                                    f"**{prefix}topic**\n"
                                                    f"You get a random Topic\n\r"
                                                    f"**{prefix}avatar <user>**\n"
                                                    f"Shows the Avatar/Icon from a User\n\r"
                                                    f"**{prefix}userid <user>**\n"
                                                    f"You get the userid from the user\n\r"
                                                    f"**{prefix}userinfo <user>**\n"
                                                    f"You get some Inforamtions about a user\n\r")
            await message.channel.purge(limit=1)
            await message.send(embed=embed, components=delete)
            res2 = await client.wait_for('button_click')
            if res2.component.label == "🗑":
                await message.channel.purge(limit=2)
                return

        if res.component.label == "Admin Commands":
            embed = discord.Embed(title="Help")
            embed.add_field(name="Admin Commands", value=f"**{prefix}ban <user> <reason>**\n"
                                                         f"Banns a User\n\r"
                                                         f"**{prefix}kick <user> <reason>**\n"
                                                         f"Kicks a  User\n\r"
                                                         f"**{prefix}unban <user>**\n"
                                                         f"Unbans a User\n\r"
                                                         f"**{prefix}settings**\n"
                                                         f"Shows the Server settings from the Bot\n\r"
                                                         f"**{prefix}clear <amount>**\n"
                                                         f"Deletes a specfic amount of Messages(only messages that are not older than 2 Weeks)")
            await message.channel.purge(limit=1)
            await message.send(embed=embed, components=delete)
            res2 = await client.wait_for('button_click')
            if res2.component.label == "🗑":
                await message.channel.purge(limit=2)
                return

        if res.component.label == "Features":
            embed = discord.Embed(title="Help")
            embed.add_field(name="Features", value=f"**Invite Deleter**\n"
                                                   f"Deletes every Invite that gets send in the chat\n\r"
                                                   f"**Message Logger**\n"
                                                   f"Loggs deleted/edited Messages in a Channel\n\r"
                                                   f"**Audit Logger**\n"
                                                   f"Loggs the audit log in a channel")
            await message.channel.purge(limit=1)
            await message.send(embed=embed, components=delete)
            res2 = await client.wait_for('button_click')
            if res2.component.label == "🗑":
                await message.channel.purge(limit=2)
                return

        if res.component.label == "🗑":
            await message.channel.purge(limit=2)
            return

    if not message.guild is None:
        settings = await guild_settings.find_one({"_id": int(message.guild.id)})
        language = settings["settings"]["language"]
        delete = [[Button(style=ButtonStyle.red, label="🗑")]]
        button = [
            [Button(style=ButtonStyle.blue, label="Commands"), Button(style=ButtonStyle.blue, label="Admin Commands"),
             Button(style=ButtonStyle.blue, label="Features")],
            Button(style=ButtonStyle.red, label="🗑")]

        prefix = client.command_prefix
        if language == "german":
            embed = discord.Embed(title="Help", description="Wozu brauchst du hilfe?")
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text="Shouganari ©")
            await message.send(embed=embed, components=button)
            res = await client.wait_for('button_click')
            if res.component.label == "Commands":
                embed = discord.Embed(title="Help")
                embed.add_field(name="Commands:", value=f"**{prefix}help**\n"
                                                        f"Zeigt diesen Command an\n\r"
                                                        f"**{prefix}info**\n"
                                                        f"Zeigt Infos über den Bot an\n\r"
                                                        f"**{prefix}code**\n"
                                                        f"Du bekommst den Source Code vom Bot\n\r"
                                                        f"**{prefix}dev**\n"
                                                        f"Zeigt Infos über den Owner/Developer vom Bot an\n\r"
                                                        f"**{prefix}topic**\n"
                                                        f"Zeigt ein Random Thema an\n\r"
                                                        f"**{prefix}guilds**\n"
                                                        f"Zeigt dir an auf wie vielen Guilden der Bot ist\n\r"
                                                        f"**{prefix}avatar <user>**\n"
                                                        f"Zeigt den Avatar/icon von einem User an\n\r"
                                                        f"**{prefix}userid <user>**\n"
                                                        f"Du bekommst die Userid vom User\n\r"
                                                        f"**{prefix}userinfo <user>**\n"
                                                        f"Du bekommst ein Paar infos über den User\n\r")

                await message.channel.purge(limit=1)
                await message.send(embed=embed, components=delete)
                res2 = await client.wait_for('button_click')
                if res2.component.label == "🗑":
                    await message.channel.purge(limit=2)
                    return

            if res.component.label == "Admin Commands":
                embed = discord.Embed(title="Help")
                embed.add_field(name="Admin Commands", value=f"**{prefix}ban <user> <reason>**\n"
                                                             f"Bannt eine Person\n\r"
                                                             f"**{prefix}kick <user> <reason>**\n"
                                                             f"Kickt eine Person\n\r"
                                                             f"**{prefix}unban <user>**\n"
                                                             f"Entbannt eine Person\n\r"
                                                             f"**{prefix}settings**\n"
                                                             f"Zeigt die Server Settings vom Bot an\n\r"
                                                             f"**{prefix}clear <amount>**\n"
                                                             f"Löscht bestimmt viele Nachrichten(Geht nur bei welchen die Unter 2 Wochen alt sind)")
                await message.channel.purge(limit=1)
                await message.send(embed=embed, components=delete)
                res2 = await client.wait_for('button_click')
                if res2.component.label == "🗑":
                    await message.channel.purge(limit=2)
                    return

            if res.component.label == "Features":
                embed = discord.Embed(title="Help")
                embed.add_field(name="Features", value=f"**Invite Deleter**\n"
                                                       f"Löscht jeden Invite im Chat\n\r"
                                                       f"**Message Logger**\n"
                                                       f"Loggt gelöschte/bearbeitete Nachrichten in einem Channel\n\r"
                                                       f"**Audit Logger**\n"
                                                       f"Loggt den Audit log in einem Channel")
                await message.channel.purge(limit=1)
                await message.send(embed=embed, components=delete)
                res2 = await client.wait_for('button_click')
                if res2.component.label == "🗑":
                    await message.channel.purge(limit=2)
                    return

            if res.component.label == "🗑":
                await message.channel.purge(limit=2)
                return
        if language == "english":
            embed = discord.Embed(title="Help", description="For what do you need Help?")
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text="Shouganari ©")
            await message.send(embed=embed, components=button)
            res = await client.wait_for('button_click')
            if res.component.label == "Commands":
                embed = discord.Embed(title="Help")
                embed.add_field(name="Commands:", value=f"**{prefix}help**\n"
                                                        f"Shows this Command\n\r"
                                                        f"**{prefix}info**\n"
                                                        f"Shows Informations about the Bot\n\r"
                                                        f"**{prefix}code**\n"
                                                        f"You can see the Source Code of Bot\n\r"
                                                        f"**{prefix}dev**\n"
                                                        f"Shows Informations about the Bot Owner/Developer\n\r"
                                                        f"**{prefix}topic**\n"
                                                        f"You get a random Topic\n\r"
                                                        f"**{prefix}guilds**\n"
                                                        f"Shows on how many guilds the bot is\n\r"
                                                        f"**{prefix}avatar <user>**\n"
                                                        f"Shows the Avatar/Icon from a User\n\r"
                                                        f"**{prefix}userid <user>**\n"
                                                        f"You get the userid from the user\n\r"
                                                        f"**{prefix}userinfo <user>**\n"
                                                        f"You get some Inforamtions about a user\n\r")
                await message.channel.purge(limit=1)
                await message.send(embed=embed, components=delete)
                res2 = await client.wait_for('button_click')
                if res2.component.label == "🗑":
                    await message.channel.purge(limit=2)
                    return

            if res.component.label == "Admin Commands":
                embed = discord.Embed(title="Help")
                embed.add_field(name="Admin Commands", value=f"**{prefix}ban <user> <reason>**\n"
                                                             f"Banns a User\n\r"
                                                             f"**{prefix}kick <user> <reason>**\n"
                                                             f"Kicks a  User\n\r"
                                                             f"**{prefix}unban <user>**\n"
                                                             f"Unbans a User\n\r"
                                                             f"**{prefix}settings**\n"
                                                             f"Shows the Server settings from the Bot\n\r"
                                                             f"**{prefix}clear <amount>**\n"
                                                             f"Deletes a specfic amount of Messages(only messages that are not older than 2 Weeks)")
                await message.channel.purge(limit=1)
                await message.send(embed=embed, components=delete)
                res2 = await client.wait_for('button_click')
                if res2.component.label == "🗑":
                    await message.channel.purge(limit=2)
                    return

            if res.component.label == "Features":
                embed = discord.Embed(title="Help")
                embed.add_field(name="Features", value=f"**Invite Deleter**\n"
                                                       f"Deletes every Invite that gets send in the chat\n\r"
                                                       f"**Message Logger**\n"
                                                       f"Loggs deleted/edited Messages in a Channel\n\r"
                                                       f"**Audit Logger**\n"
                                                       f"Loggs the audit log in a channel")
                await message.channel.purge(limit=1)
                await message.send(embed=embed, components=delete)
                res2 = await client.wait_for('button_click')
                if res2.component.label == "🗑":
                    await message.channel.purge(limit=2)
                    return

            if res.component.label == "🗑":
                await message.channel.purge(limit=2)
                return


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` **loaded**")


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` **unloaded**")


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await asyncio.sleep(3)
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` **reloaded**")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(Token)
