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

class Cogs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        logs = logs[0]
        settings = await guild_settings.find_one({"_id": int(guild.id)})
        audit_status = settings["settings"]["audit"]["status"]
        audit_channelid = settings["settings"]["audit"]["channelid"]
        audit_channel = self.client.get_guild(audit_channelid)
        user2 = await self.client.fetch_user(user.id)
        if audit_status == "enable" and audit_channel is not None:
            if not user.bot:
                embed = discord.Embed(
                    title="Bann",
                    color=discord.Color.red())
                embed.add_field(name="Banned User", value=user.name, inline=True)
                embed.add_field(name="Banned By", value=logs.user.mention, inline=True)
                embed.add_field(name="Reason", value=logs.reason, inline=False)
                embed.set_thumbnail(url=user2.avatar_url)
                embed.timestamp = logs.created_at
                await audit_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        logs = logs[0]
        settings = await guild_settings.find_one({"_id": int(guild.id)})
        audit_status = settings["settings"]["audit"]["status"]
        audit_channelid = settings["settings"]["audit"]["channelid"]
        audit_channel = self.client.get_guild(audit_channelid)
        user2 = await self.client.fetch_user(user.id)
        if audit_status == "enable" and audit_channel is not None:
            embed = discord.Embed(
                title="Unbann",
                color=discord.Color.green())
            embed.add_field(name="Unbanned User", value=user.name, inline=True)
            embed.add_field(name="Unbanned By", value=logs.user.mention, inline=True)
            embed.set_thumbnail(url=user2.avatar_url)
            embed.timestamp = logs.created_at
            await audit_channel.send(embed=embed)

def setup(client):
    client.add_cog(Cogs(client))
