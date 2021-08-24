import json
import os
import typing
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption)
import psutil
from PIL import Image, ImageDraw, ImageChops, ImageFont
import discord
from discord.ext import commands
from io import BytesIO
import datetime

with open("./config.json", "r") as config:
    config = json.load(config)


def circle(pfp, size=(215, 215)):
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


class infos(commands.Cog, description="Informations about the Bot and much more"):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.dev_only = False

    @commands.command(help="Shows the Bot Badges from a User")
    async def badges(self, ctx, user: typing.Union[discord.User, str] = None):
        if user is None:
            #user_find = await users.find_one({"_id": int(ctx.author.id)})

            #if ctx.author.id == user_find:
            print("Test")

            #else:
             #   await ctx.send("You don't have badges")

        else:
            #user_find = await users.find_one({"_id": int(user.id)})

            #if user.id == user_find:
            print("Test")
           # else:
            #    await ctx.reply.send("This Person don't have badges", mention_author=False)

    @commands.command(help="Gets a Users Avatar")
    @commands.guild_only()
    async def avatar(self, message, args1: discord.Member):
        embed = discord.Embed(title=f"{args1.name}'s Avatar", color=discord.Color.blue())
        embed.timestamp = datetime.datetime.now()
        embed.set_image(url=args1.avatar_url)
        await message.send(embed=embed)


    @commands.command(help="Shows Informations about a User")
    async def userinfo(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author

        name, nick, Id, status = str(member), member.display_name, str(member.id), str(member.status).upper()

        highestrole = str(member.top_role.name)

        administrator = ""

        created_at = member.created_at.strftime("%a %b\n%B %Y")
        joined_at = member.joined_at.strftime("%a %b\n%B %Y")

        base = Image.open(".\\locales\\img\\base.png").convert("RGBA")
        background = Image.open(".\\locales\\img\\banner.png").convert("RGBA")

        pfp = member.avatar_url_as(size=256)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")

        name = f"{name[:16]}.." if len(name) > 16 else name
        nick = f"AKA - {nick[:17]}.." if len(nick) > 17 else f"AKA -{nick}"
        highestrole = f"{highestrole[:15]}.." if len(highestrole) > 15 else highestrole
        if member.guild_permissions.administrator:
            administrator += "True"
        if not member.guild_permissions.administrator:
            administrator += "False"
        draw = ImageDraw.Draw(base)
        pfp = circle(pfp, size=(215, 215))
        font = ImageFont.truetype("./locales/fonts/Roboto-Black.ttf", 38)
        akafont = ImageFont.truetype("./locales/fonts/Roboto-Black.ttf", 30)
        subfont = ImageFont.truetype("./locales/fonts/Roboto-Black.ttf", 25)

        draw.text((280, 240), name, font=font)
        draw.text((270, 315), nick, font=akafont)
        draw.text((65, 490), Id, font=subfont)
        draw.text((405, 490), status, font=subfont)
        draw.text((65, 635), highestrole, font=subfont)
        draw.text((405, 635), administrator, font=subfont)
        draw.text((65, 770), created_at, font=subfont)
        draw.text((405, 770), joined_at, font=subfont)
        base.paste(pfp,(56, 158), pfp)

        background.paste(base, (0, 0), base)
        with BytesIO() as a:
            background.save(a, "PNG")
            a.seek(0)
            await ctx.send(file=discord.File(a, "profile.png"))

    @commands.command(help="About the Bot")
    async def about(self, ctx):
        buttons = [[Button(style=ButtonStyle.URL,
                         url="https://discord.com/api/oauth2/authorize?client_id=867108673146847272&permissions=8&scope=bot",
                         label="Invite"), Button(style=ButtonStyle.URL, url="https://github.com/Shouganari/Chifuyu-Matsuno", label="Source Code")]]

        embed = discord.Embed(title=f"Info about Chifuyu Matsuno")
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
        await ctx.send(embed=embed, components=buttons)

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

    @commands.command(help="Shows on how many Guilds the Bot is on")
    async def guilds(self, message):
        embed = discord.Embed(title="Guilds")
        embed.add_field(name="Guild Count", value=f"{len(self.client.guilds)} Guilds")
        button = [
            Button(style=ButtonStyle.URL, url="https://github.com/Shouganari/Chifuyu-Matsuno/", label="Source Code")]
        await message.send(embed=embed, components=button)

    @commands.command(help="Shows how many Users using the Bot")
    async def users(self, message):
        embed = discord.Embed(title="Users")
        embed.add_field(name="User Count", value=f"{len(self.client.users)} Users")
        button = [
            Button(style=ButtonStyle.URL, url="https://github.com/Shouganari/Chifuyu-Matsuno/", label="Source Code")]
        await message.send(embed=embed, components=button)

    @commands.command(help="Shows Informations About the Owner/Developer of the Bot")
    async def dev(self, message):
        chifuyu = self.client.get_user(867108673146847272)
        yuutakatabot = self.client.get_user(831153299570425866)
        yokaisbot = self.client.get_user(856505439034146847)
        me = self.client.get_user(437669166216904715)
        embed = discord.Embed(
            title=f"Developer Info {config['emoji']['dev']}")
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


def setup(client):
    client.add_cog(infos(client))
