import discord
from discord.ext import commands
import datetime
import json

with open("./config.json", "r") as config:
    config = json.load(config)


class mod(commands.Cog, description=f"Commands for Moderators from a Server"):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.dev_only = False


    @commands.command()
    async def warn(self, message, args1: discord.Member, *, args):
        print("test")


def setup(client):
    client.add_cog(mod(client))