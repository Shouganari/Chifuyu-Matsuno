from discord.ext import commands
import discord
import datetime


class Cogs(commands.Cog):

    def __init__(self, client):
        self.client = client



    @commands.command()
    async def info(self, message):
        bot = self.client.get_user(867108673146847272)
        me = self.client.get_user(437669166216904715)
        embed = discord.Embed(
            title="Bot Info", description=f"If you want to get more info about the Owner/Developer do **{self.client.command_prefix}dev** or **/dev**")
        embed.add_field(name="Prefix", value=f"`{self.client.command_prefix} or /`\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Latency", value=f"`{round(self.client.latency * 1000)}ms`\n⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Developer", value=f"**[{me.name}](https://discord.com/users/437669166216904715)**\n⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Code Language", value="**Python**\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Api", value="**Discord.py**\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Bot Version", value="**1.0.0 Beta**\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Creation Date", value="**__<t:1626739200:d>__**", inline=True)
        embed.add_field(name="Release Date", value="`None`", inline=True)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Chifuyu Matsuno", icon_url=bot.avatar_url)
        embed.set_thumbnail(url=bot.avatar_url)
        await message.send(embed=embed)

    @commands.command()
    async def dev(self, message):
        chifuyu = self.client.get_user(867108673146847272)
        yuutakatabot = self.client.get_user(831153299570425866)
        yokaisbot = self.client.get_user(856505439034146847)
        me = self.client.get_user(437669166216904715)
        embed = discord.Embed(
            title="Developer Info")
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
    async def Code(self, message):
        embed = discord.Embed(
            title="Source Code", color=discord.Color.light_grey())
        embed.add_field(name="Github", value="[Source Code](https://github.com/Yuutokata/Chifuy-Matsuno)", inline=False)
        embed.add_field(name="License", value="You can use the Code in your Code but just please don't say that you codet it", inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/867501733084135474/867502083086483497/GitHub-Mark-Light-120px-plus.png")
        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/867501733084135474/867502083086483497/GitHub-Mark-Light-120px-plus.png", text="Github Code")
        await message.send(embed=embed)

    @commands.command()
    async def userinfo(self, message, args1 : discord.Member):
        embed = discord.Embed(
            title=args1,
            description=args1.mention)
        embed.add_field(name="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀__ID__", value=f"```⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{args1.id}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀```\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=False)
        embed.add_field(name="Registered", value=f"<t:{round(args1.created_at.timestamp())}:d>\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Joined", value=f"<t:{round(args1.joined_at.timestamp())}:d>\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.add_field(name="Highest Role", value=f"{args1.top_role.mention}\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=True)
        embed.set_thumbnail(url=args1.avatar_url)
        embed.set_footer(icon_url=args1.avatar_url, text=args1.name)
        embed.timestamp = datetime.datetime.now()
        await message.send(embed=embed)

    @commands.command()
    async def userid(self, message, args1 : discord.Member):
        embed = discord.Embed(
            title=args1.name, description=args1.mention)
        embed.add_field(name="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀__ID__", value=f"```⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀{args1.id}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀```\n⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀", inline=False)
        embed.set_thumbnail(url=args1.avatar_url)
        embed.timestamp = datetime.datetime.now()
        await message.send(embed=embed)

def setup(client):
    client.add_cog(Cogs(client))
