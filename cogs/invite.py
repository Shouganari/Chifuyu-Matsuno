import datetime

import discord
from discord.ext import commands

from utils.mongo import guild_settings


class Invite(commands.Cog, name="Invite"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        settings = await guild_settings.find_one({"_id": int(message.guild.id)})
        invite_status = settings["settings"]["invite"]["status"]
        invite_role = settings["settings"]["invite"]["role1"]
        channelid = settings["settings"]["invite"]["channelid"]
        language = settings["settings"]["language"]
        if invite_status == "enable":
            if 'discord.gg' in message.content or 'discord.com' in message.content:
                if invite_role == "None":
                    if not message.author.guild_permissons.adminstator:
                        await message.delete()
                        embedde = discord.Embed(
                            title="Self Promotion",
                            description=f"{message.author.mention} Bitte mache keine Eigenwerbung",
                            color=discord.Color.blue())
                        embedde.set_footer(text="Yuutokata © 2021")
                        embedde.timestamp = datetime.datetime.now()
                        embeden = discord.Embed(
                            title="Self Promotion",
                            description=f"{message.author.mention} Bitte mache keine Eigenwerbung",
                            color=discord.Color.blue())
                        embeden.set_footer(text="Yuutokata © 2021")
                        embeden.timestamp = datetime.datetime.now()
                        if language == "german":
                            await message.channel.send(embed=embedde, delete_after=60)
                        if language == "english":
                            await message.channel.send(embed=embeden, delete_after=60)
                if not invite_role == "None":
                    role = discord.utils.get(message.guild.roles, id=int(invite_role))
                    if message.author not in role.members:
                        await message.delete()
                        embedde = discord.Embed(
                            title="Self Promotion",
                            description=f"{message.author.mention} Bitte mache keine Eigenwerbung",
                            color=discord.Color.blue())
                        embedde.set_footer(text="Yuutokata © 2021")
                        embedde.timestamp = datetime.datetime.now()
                        embeden = discord.Embed(
                            title="Self Promotion",
                            description=f"{message.author.mention} Dont do Self Promotion",
                            color=discord.Color.blue())
                        embeden.set_footer(text="Yuutokata © 2021")
                        embeden.timestamp = datetime.datetime.now()
                        if language == "german":
                            if channelid == "None":
                                await message.channel.send(embed=embedde, delete_after=60)
                            if not channelid == "None":
                                await message.channel.send(embed=embedde, delete_after=60)
                                channel = discord.utils.get(message.guild.text_channels, id=channelid)
                                embed = discord.Embed(title="Invite Deleter", color=discord.Color.red())
                                embed.add_field(name="Content", value=message.content, inline=True)
                                embed.add_field(name="Person", value=f"{message.author.name} | {message.author.id}")
                                await channel.send(embed=embed)

                        if language == "english":
                            if channelid == "None":
                                await message.channel.send(embed=embedde, delete_after=60)
                            if not channelid == "None":
                                await message.channel.send(embed=embedde, delete_after=60)
                                channel = discord.utils.get(message.guild.text_channels, id=channelid)
                                embed = discord.Embed(title="Invite Deleter", color=discord.Color.red())
                                embed.add_field(name="Content", value=message.content, inline=True)
                                embed.add_field(name="Person", value=f"{message.author.name} | {message.author.id}")
                                await channel.send(embed=embed)


def setup(client):
    client.add_cog(Invite(client))
