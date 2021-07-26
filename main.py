import discord
from discord.ext import commands
import json
import os
import asyncio
from discord_components import DiscordComponents

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

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` wurde **geladen**")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` wurde **entladen**")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await asyncio.sleep(3)
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"`{extension}` wurde **neugeladen**")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(Token)
