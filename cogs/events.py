import typing
from utils.mongo import settings
import discord
from discord.ext import commands
import datetime
import json
import re

with open("./config.json", "r") as config:
    config = json.load(config)


def get_invites(message):
    INVITE = "discord(?:\.com|app\.com|\.gg)/(?:invite/)?([a-zA-Z0-9\-]{2,32})"
    regex = re.compile(INVITE)
    invites = regex.findall(message)
    if regex.match(message):
        return True
    else:
        return False


class events(commands.Cog, description="Just a few Events"):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.dev_only = False

    @commands.Cog.listener()
    async def on_message(self, message):
        check_quote = re.compile(
            r'https?://(?:(ptb|canary|www)\.)?discord(?:app)?\.com/channels/'
            r'(?:[0-9]{15,21}|@me)'
            r'/(?P<channel_id>[0-9]{15,21})/(?P<message_id>[0-9]{15,21})/?$')
        check_invite = re.compile(r'discord(?:\.com|app\.com|\.gg)/(?:invite/)?([a-zA-Z0-9\-]{2,32})')
        if check_quote.match(message.content):
            x = re.compile(r'(?:(?P<channel_id>[0-9]{15,21})/)?(?P<message_id>[0-9]{15,21})$')
            y = x.search(f'{message.content}')
            channel_id = y.group('channel_id')
            channel = self.client.get_channel(int(channel_id))
            message_id = y.group('message_id')
            msg = await channel.fetch_message(int(message_id))
            embed = discord.Embed(title="Auto Quote",
                                  description=f"If you want to disable this do `{self.client.command_prefix}quote <off/on>`",
                                  color=int(config["colors"]["Main"]))
            embed.add_field(name="Content:", value=msg.content, inline=False)
            embed.add_field(name="By", value=msg.author.name, inline=False)
            await message.reply(embed=embed, mention_author=False)
        elif check_invite.search(message.content):
            if not message.author.guild_permissions.administrator:
                embed = discord.Embed(title="Server Invite", description=f"You send an Invite in the chat from {message.guild.name}. Don't do that again", color=int(config["colors"]["ERROR"]))
                await message.author.send(embed=embed)
                await message.delete()
            else:
                return

    #@commands.Cog.listener()
   # async def on_member_update(self, before, after):
        #boost = await settings.find_one({"_id", int(after.guild.id)})
        #if boost["status"] is True:



def setup(client):
    client.add_cog(events(client))
