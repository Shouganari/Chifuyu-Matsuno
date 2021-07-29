import datetime
import os

import discord
import psutil
from discord.ext import commands
from discord_components import (
    Button,
    ButtonStyle)

from utils.emoji import *


class Commands(commands.Cog, name="Commands"):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dev(self, message):
        chifuyu = self.client.get_user(867108673146847272)
        yuutakatabot = self.client.get_user(831153299570425866)
        yokaisbot = self.client.get_user(856505439034146847)
        me = self.client.get_user(437669166216904715)
        embed = discord.Embed(
            title=f"Developer Info {discordCoder}")
        embed.add_field(name="Name", value=f"**{me.name}**\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Account Creation Date", value=f"__<t:1524355200:d>__\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Links", value="__[My Links](https://links.yuuto.de/)__\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="More Bots", value=f"{chifuyu.name}\n"
                                                f"{yuutakatabot.name}\n"
                                                f"__{yokaisbot.name}__\n", inline=True)
        embed.set_thumbnail(url=me.avatar_url)
        embed.set_footer(icon_url=me.avatar_url, text=me.name)
        embed.timestamp = datetime.datetime.now()
        await message.send(embed=embed)

    @commands.command()
    async def code(self, message):
        embed = discord.Embed(
            title=f"Source Code {github_emoji}", color=discord.Color.light_grey())
        embed.add_field(name="Github", value="[Source Code](https://github.com/Yuutokata/Chifuy-Matsuno)", inline=False)
        embed.add_field(name="License",
                        value="You can use the Code in your Code but just please don't say that you codet it",
                        inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/867501733084135474/867502083086483497/GitHub-Mark-Light-120px-plus.png")
        embed.set_footer(
            icon_url="https://cdn.discordapp.com/attachments/867501733084135474/867502083086483497/GitHub-Mark-Light-120px-plus.png",
            text="Shouganari ©")
        await message.send(embed=embed)

    @commands.command()
    async def userinfo(self, message, args1: discord.Member):
        embed = discord.Embed(
            title=args1,
            description=args1.mention)
        embed.add_field(name="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀__ID__", value=f"```⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{args1.id}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀```\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
                        inline=False)
        embed.add_field(name="Registered", value=f"<t:{round(args1.created_at.timestamp())}:d>\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
                        inline=True)
        embed.add_field(name="Joined", value=f"<t:{round(args1.joined_at.timestamp())}:d>\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Highest Role", value=f"{args1.top_role.mention}\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.set_thumbnail(url=args1.avatar_url)
        embed.set_footer(icon_url=args1.avatar_url, text=args1.name)
        embed.timestamp = datetime.datetime.now()
        await message.send(embed=embed)

    @commands.command()
    async def userid(self, message, args1: discord.Member):
        embed = discord.Embed(
            title=args1.name, description=args1.mention)
        embed.add_field(name="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀__ID__", value=f"```⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{args1.id}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀```\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
                        inline=False)
        embed.set_thumbnail(url=args1.avatar_url)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Shouganari ©")
        await message.send(embed=embed)

    @commands.command()
    async def guilds(self, message):
        embed = discord.Embed(title="Guilds")
        embed.add_field(name="Guild Count", value=f"{len(self.client.guilds)} Guilds")
        button = [
            Button(style=ButtonStyle.URL, url="https://github.com/Shouganari/Chifuyu-Matsuno/", label="Source Code")]
        await message.send(embed=embed, components=button)

    @commands.command()
    async def users(self, message):
        embed = discord.Embed(title="Users")
        embed.add_field(name="User Count", value=f"{len(self.client.users)} Users")
        button = [
            Button(style=ButtonStyle.URL, url="https://github.com/Shouganari/Chifuyu-Matsuno/", label="Source Code")]
        await message.send(embed=embed, components=button)

    @commands.command()
    async def about(self, ctx):
        button = [Button(style=ButtonStyle.URL,
                         url="https://discord.com/api/oauth2/authorize?client_id=867108673146847272&permissions=8&scope=bot",
                         label="Invite")]
        embed = discord.Embed(title=f"Info about Chifuyu Matsuno")
        embed.add_field(
            name="Latest Updates",
            value="Vote Now at [top.gg](https://top.gg/bot/756257170521063444/vote)",
            inline=False)
        pid = psutil.Process(os.getpid())
        used = pid.memory_info().rss / 1024 ** 2
        total = psutil.virtual_memory().total / 1024 ** 2
        bot = self.client.get_user(867108673146847272)
        developer = self.client.get_user(437669166216904715)
        embed.add_field(name="Developer", value=f"[{developer.name}](https://discord.com/users/437669166216904715)")
        embed.add_field(name="Code Language", value="**Python**")
        embed.add_field(name="Bot Version", value="**1.0.0 Beta**")
        embed.add_field(name="Creation Date", value="**__<t:1626739200:d>__**")
        embed.add_field(name="Release Date", value="`None`")
        embed.add_field(name="Ping", value=f"`{round(self.client.latency * 1000)}ms`")
        embed.add_field(name="Guild Count", value=f"{len(self.client.guilds)} Guilds")
        embed.add_field(name="User Count", value=f"{len(self.client.users)} Users")
        embed.add_field(name="CPU Usage", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="Memory Usage", value=f"{used:,.2f}/{round(total)} MB")
        embed.add_field(
            name="Bot Invite",
            value=f"Not Released",
        )
        embed.add_field(name="Commands", value=f"{len(self.client.commands)} loaded")
        credits_list = [
            (self.client.get_user(437669166216904715), 'Owner/Developer'),
            (self.client.get_user(774286355580583957), 'Tester'),
        ]
        embed.add_field(
            name="Credits",
            value="\n\r".join(f"{user} ({role})" for user, role in credits_list)
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Shouganari ©", icon_url=bot.avatar_url)
        embed.set_thumbnail(url=bot.avatar_url)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
