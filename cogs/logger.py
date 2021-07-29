import discord
from discord.ext import commands
import asyncio
import json
import datetime
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption)
from utils.mongo import guild_settings
import datetime


class Logger(commands.Cog, name="Logger"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, before):
        settings = await guild_settings.find_one({"_id": int(before.guild.id)})
        logger_status = settings["settings"]["logger"]["status"]
        logger_channel = settings["settings"]["logger"]["channelid"]
        if logger_status == "enable" and not logger_channel == "None":
            if not before.author.bot:
                embed = discord.Embed(title="Message Deleted", color=discord.Color.red(), url=before.jump_url)
                embed.add_field(name="Message Author", value=before.author.name, inline=True)
                embed.add_field(name="Time", value=f"<t:{datetime.datetime.now().timestamp()}:d>", inline=True)
                embed.add_field(name="Content", value=before.content, inline=False)
                embed.set_footer(text="Shouganari ©")
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=before.author.avatar_url)
                channel = self.client.get_channel(int(logger_channel))
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        settings = await guild_settings.find_one({"_id": int(before.guild.id)})
        logger_status = settings["settings"]["logger"]["status"]
        logger_channel = settings["settings"]["logger"]["channelid"]
        if logger_status == "enable" and not logger_channel == "None":
            if not before.author.bot:
                embed = discord.Embed(title="Message Edited", color=discord.Color.orange(), url=after.jump_url)
                embed.add_field(name="Message Author", value=before.author.name, inline=True)
                embed.add_field(name="Time", value=f"<t:{datetime.datetime.now().timestamp()}:d>", inline=True)
                embed.add_field(name=f"\u200B", value="\u200B", inline=True)
                embed.add_field(name="Before Content", value=before.content, inline=True)
                embed.add_field(name="After Content", value=after.content, inline=True)
                embed.timestamp = datetime.datetime.now()
                embed.set_thumbnail(url=before.author.avatar_url)
                channel = self.client.get_channel(logger_channel)
                await channel.send(embed=embed)



def setup(client):
    client.add_cog(Logger(client))
