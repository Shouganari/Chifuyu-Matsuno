import discord
from discord.ext import commands
import json
import os
import asyncio
from discord_components import DiscordComponents
import motor.motor_asyncio
from utils.mongo import db, guild_settings


with open("config.json", "r") as f:
    config = json.load(f)

Token = config["Token"]
activity = discord.Activity(type=discord.ActivityType.listening, name="ch!")
intents = discord.Intents.all()
client = commands.Bot(command_prefix="ch!", intents=intents, activity=activity, status=discord.Status.online)

@client.event
async def on_ready():
    print("Bot on")
    DiscordComponents(client)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(Token)
