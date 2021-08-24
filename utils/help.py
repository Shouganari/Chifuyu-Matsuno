import discord
from discord import colour
from discord.ext import commands
from utils.mongo import settings
import datetime
import json
from utils.checks import is_dev
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption)

with open("./config.json", "r") as config:
    config = json.load(config)

with open("./news.json", "r") as news:
    news = json.load(news)

async def get_cog_help(cog, context):
    server = config["links"]["Support-Server"]
    vote = config["links"]["Vote-Link"]
    invite = config["links"]["Invite-Link"]
    cog = context.bot.get_cog(cog.lower())
    embed = discord.Embed(title=f"{cog.qualified_name.title()} Catagory", color=int(config["colors"]["Main"]))
    embed.set_thumbnail(url=context.bot.user.avatar_url)
    embed.add_field(name="\u200B", value=f"[Support Server]({server}) | [Vote Link]({vote}) | [Invite Link]({invite})")

    empty = ""
    comds = cog.get_commands()

    for e in comds:
        empty += f"`{context.bot.command_prefix}{e.name}` - {e.help}\n"

        embed.description = f"To get detailed help, please use `{context.bot.command_prefix}help <cmd>`\n\n**Commands:**\n{empty}"

    return embed


class ChifuyuHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        shouganari_links = config["links"]["Shouganari-Links"]
        server = config["links"]["Support-Server"]
        vote = config["links"]["Vote-Link"]
        invite = config["links"]["Invite-Link"]
        buttons = [[Button(style=ButtonStyle.URL, label="Support Server", url=server), Button(style=ButtonStyle.URL, label="Vote for us", url=vote), Button(style=ButtonStyle.URL, label="Invite Link", url=invite)]]
        embed = discord.Embed(
            title="Help Command",
            description=f"Hey, I'm a Discord bot by [Shouganari]({shouganari_links})\n To get the commands of a Categorie use `{self.context.bot.command_prefix}help <category>`",
            color=int(config["colors"]["Main"]))
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url=self.context.bot.user.avatar_url)
        embed.set_footer(text=f"Shouganari ©")
        empty = ""
        for cogs in self.context.bot.cogs:
            cog = self.context.bot.get_cog(cogs)
            if cog.hidden:
                pass
            elif cog.dev_only:
                if is_dev():
                    empty += f"`{cog.qualified_name}` | {cog.description} | **{len(cog.get_commands())}**\n\r"
            elif not cog.dev_only and not cog.hidden:
                empty += f"`{cog.qualified_name}` | {cog.description} | **{len(cog.get_commands())}**\n\r"

        embed.add_field(name="__Categorie's__", value=f" ⠀ \n{empty}", inline=False)
        if news['send'] == "True":
            embed.add_field(name=f"{config['emoji']['announcment']} __Latest News from {news['time']}__", value=f"{news['news']}")

        await self.context.reply(embed=embed, components=buttons, mention_author=False)

    async def send_command_help(self, command):
        server = config["links"]["Support-Server"]
        vote = config["links"]["Vote-Link"]
        invite = config["links"]["Invite-Link"]
        empty = ""
        aliases = ""
        buttons = [[Button(style=ButtonStyle.URL, label="Support Server", url=server), Button(style=ButtonStyle.URL, label="Vote for us", url=vote), Button(style=ButtonStyle.URL, label="Invite Link", url=invite)]]
        for cancer in command.clean_params:
            empty += f"<{cancer}> "
        for alias in command.aliases:
            aliases += f"`{alias}` "
        embed = discord.Embed(
            title=f"{command.name.title()} Help",
            description=f"{command.help}\n"
                        f" **Usage:**\n"
                        f"{self.context.bot.command_prefix}{command.name} {empty}\n"
                        f"**Aliases:** {aliases if len(aliases) > 0 else 'None'}\n"
                        f"**Cooldown:** {0 if command._buckets._cooldown == None else command._buckets._cooldown.per} seconds",
            color=int(config["colors"]["Main"]),
            timestamp=datetime.datetime.now())
        embed.set_footer(text=f"Shouganari ©")

        await self.context.reply(embed=embed, components=buttons, mention_author=False)

    async def send_cog_help(self, cog):
        await self.context.reply(embed=await get_cog_help(cog.qualified_name, self.context), mention_author=False)

    async def send_group_help(self, group):
        pass

    async def send_error_message(self, error):
        emoji = config["emoji"]["Error"]
        embed = discord.Embed(
            name=f"{emoji} Error!",
            color=int(config["colors"]["error"]),
            description=error)
        await self.context.reply(embed=embed, mention_author=False)
