import typing
from utils.mongo import settings
import discord
from discord.ext import commands
import datetime
import json
import re

with open("./config.json", "r") as config:
    config = json.load(config)


ANTIHOIST_CHARS = ["!", "?", "@", "#", "$", "%", "^", "&", "*", "+", "=", ".", ",", ";", ":", "`", "~", "'", '"', "\\", "/", "|"]

class antihoasting(commands.Cog, description="Antihoasting"):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.dev_only = False

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if after.bot:
            return
        protection = await settings.find_one({"_id": int(after.guild.id)})
        if protection["protection"]["anti-hoasting"]["status"] is True:
            if protection["protection"]["anti-hoasting"]["role"] is not False:
                role = discord.utils.get(after.guild.roles, id=int(protection["protection"]["anti-hoasting"]["role"]))
                if after in role.members:
                    return
                if after.display_name.startswith() and not after.display_name.startswith("[AFK]"):
                    try:
                        if before.display_name[0] not in ANTIHOIST_CHARS:
                            await after.edit(
                                nick=before.display_name,
                                reason="Antihoisting")
                        else:
                            await after.edit(
                                nick="Moderated Nickname",
                                reason="Antihoisting")
                    except Exception:
                        pass

            if protection["protection"]["anti-hoasting"]["role"] is False:
                if after.display_name[0] in ANTIHOIST_CHARS and not after.display_name.startswith("[AFK]"):
                    try:
                        if before.display_name[0] not in ANTIHOIST_CHARS:
                            await after.edit(
                                nick=before.display_name,
                                reason="Antihoisting")
                        else:
                            await after.edit(
                                nick="Moderated Nickname",
                                reason="Antihoisting")

                    except Exception:
                        pass


def setup(client):
    client.add_cog(antihoasting(client))