import discord
from discord.ext import commands
import json
import os
import asyncio
from discord_components import DiscordComponents
import motor.motor_asyncio

cluster = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://<username>t:<passwort>@discord.mz3vr.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["Discord"]
guild_settings = db["guild settings"]
