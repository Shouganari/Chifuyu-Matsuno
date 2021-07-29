import asyncio
from discord.ext import commands, tasks
import discord
import datetime
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption)
import json
from utils.mongo import cluster, db, guild_settings
import motor.motor_asyncio

with open("./setup.json", "r") as file:
    data = json.load(file)


class Cogs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["purge"])
    async def clear(self, message, num: int, user: discord.User = None):
        settings = await guild_settings.find_one({"_id": int(message.guild.id)})
        language = settings["settings"]["language"]
        team_id = settings["settings"]["team role"]
        if not team_id == "None":
            team_role = discord.utils.get(message.guild.roles, id=team_id)
            if language == "german":
                if message.author.guild_permissions.manage_messages or message.author in team_role.members:
                    if user:
                        check_func = lambda msg: msg.author == user and not msg.pinned
                    else:
                        check_func = lambda msg: not msg.pinned

                    await message.message.delete()
                    await message.channel.purge(limit=num, check=check_func)
                    await message.send(f'{num} Nachrichten gelöscht', delete_after=5)
            if language == "english":
                if message.author.guild_permissions.manage_messages or message.author in team_role.members:
                    if user:
                        check_func = lambda msg: msg.author == user and not msg.pinned
                    else:
                        check_func = lambda msg: not msg.pinned

                    await message.message.delete()
                    await message.channel.purge(limit=num, check=check_func)
                    await message.send(f'{num} messages deleted', delete_after=5)

        if team_id == "None":
            if language == "german":
                if message.author.guild_permissions.manage_messages:
                    if user:
                        check_func = lambda msg: msg.author == user and not msg.pinned
                    else:
                        check_func = lambda msg: not msg.pinned

                    await message.message.delete()
                    await message.channel.purge(limit=num, check=check_func)
                    await message.send(f'{num} Nachrichten gelöscht', delete_after=5)
            if language == "english":
                if message.author.guild_permissions.manage_messages:
                    if user:
                        check_func = lambda msg: msg.author == user and not msg.pinned
                    else:
                        check_func = lambda msg: not msg.pinned

                    await message.message.delete()
                    await message.channel.purge(limit=num, check=check_func)
                    await message.send(f'{num} messages deleted', delete_after=5)


    @commands.command()
    async def ban(self, message, args1: discord.Member, *, reason):
        button1 = [[Button(style=ButtonStyle.green, label="Yes"), Button(style=ButtonStyle.red, label="No")]]
        button2 = [[Button(style=ButtonStyle.green, label="Ja"), Button(style=ButtonStyle.red, label="Nein")]]
        settings = await guild_settings.find_one({"_id": int(message.guild.id)})
        language = settings["settings"]["language"]
        team_id = settings["settings"]["team role"]
        if not team_id == "None":
            team_role = discord.utils.get(message.guild.roles, id=team_id)
            if language == "german":
                if message.author.guild_permissions.ban_members or message.autor in team_role.members:
                    if not message.author.id == args1.id:
                        m = await message.send(f"Bist du dir sicher das du {args1} bannen willst für {reason}?", components=[button2])
                        res = await self.client.wait_for('button_click')
                        if res.component.label == "Ja":
                            await message.delete(m)
                            target = await self.client.fetch_user(args1.id)
                            dm = await target.create_dm()
                            embedm = discord.Embed(
                                    title="Bann",
                                    description=f"Du wurdest von {message.guild.name} gebannt",
                                    color=discord.Color.red())
                            embedm.add_field(name="Gebannt von", value=message.author, inline=True)
                            embedm.add_field(name="Reason", value=reason, inline=True)
                            embedm.timestamp = datetime.datetime.now()
                            embedm.set_image(url=target.avatar_url)
                            await dm.send(embed=embedm)
                            embed = discord.Embed(
                                    title="Ban",
                                    color=discord.Color.blue())
                            embed.add_field(name="Gebannte Person", value=args1.mention, inline=True)
                            embed.add_field(name="Gebannt von", value=message.author.mention, inline=True)
                            embed.add_field(name="Reason", value=reason, inline=False)
                            embed.set_thumbnail(url=target.avatar_url)
                            embed.timestamp = datetime.datetime.now()
                            await message.send(embed=embed)
                            await message.guild.ban(args1, reason=reason)
                            await message.send("Ban completed", delete_after=5)

                        if res.component.label == "Nein":
                            await message.send("Ban wurde abgebrochen")
                            await asyncio.sleep(3)
                            await message.channel.purge(limit=3)
                            return

                    if message.author.id == args1.id:
                        await message.send("Du kannst dich nicht selbst bannen")
                        return
                if not message.author.guild_permissions.ban_members and not message.author in team_role.members:
                    await message.send("Du hast nicht genug **Berechtigungen** für diesen Command\n"
                                           "```Benötigte Permissions = Ban Members```")

            if language == "english":
                if message.author.guild_permissions.ban_members or message.autor in team_role.members:
                    if not message.author.id == args1.id:
                        m = await message.send(f"Are you sure to ban {args1} for {reason}?",
                                               components=[button1])
                        res = await self.client.wait_for('button_click')
                        if res.component.label == "Yes":
                            await message.delete(m)
                            target = await self.client.fetch_user(args1.id)
                            dm = await target.create_dm()
                            embedm = discord.Embed(
                                title="Ban",
                                description=f"You got banned from {message.guild.name}",
                                color=discord.Color.red())
                            embedm.add_field(name="Banned by", value=message.author, inline=True)
                            embedm.add_field(name="Reason", value=reason, inline=True)
                            embedm.timestamp = datetime.datetime.now()
                            embedm.set_image(url=target.avatar_url)
                            await dm.send(embed=embedm)
                            embed = discord.Embed(
                                title="Ban",
                                color=discord.Color.blue())
                            embed.add_field(name="Banned Person", value=args1.mention, inline=True)
                            embed.add_field(name="Banned by", value=message.author.mention, inline=True)
                            embed.add_field(name="Reason", value=reason, inline=False)
                            embed.set_thumbnail(url=target.avatar_url)
                            embed.timestamp = datetime.datetime.now()
                            await message.send(embed=embed)
                            await message.guild.ban(args1, reason=reason)
                            await message.send("Ban completed", delete_after=5)

                        if res.component.label == "No":
                            await message.send("Ban stopped")
                            await asyncio.sleep(3)
                            await message.channel.purge(limit=3)
                            return

                    if message.author.id == args1.id:
                        await message.send("You can't ban yourself")
                        return
                if not message.author.guild_permissions.ban_members and not message.author in team_role.members:
                    await message.send("You don't have enough **Permissions** to do that Command\n"
                                       "````Required Permissions = Ban Members```")

        if team_id == "None":
            if language == "german":
                if message.author.guild_permissions.ban_members:
                    if not message.author.id == args1.id:
                        m = await message.send(f"Bist du dir sicher das du {args1} bannen willst für {reason}?", components=[button2])
                        res = await self.client.wait_for('button_click')
                        if res.component.label == "Ja":
                            await message.delete(m)
                            target = await self.client.fetch_user(args1.id)
                            dm = await target.create_dm()
                            embedm = discord.Embed(
                                    title="Bann",
                                    description=f"Du wurdest von {message.guild.name} gebannt",
                                    color=discord.Color.red())
                            embedm.add_field(name="Gebannt von", value=message.author, inline=True)
                            embedm.add_field(name="Reason", value=reason, inline=True)
                            embedm.timestamp = datetime.datetime.now()
                            embedm.set_image(url=target.avatar_url)
                            await dm.send(embed=embedm)
                            embed = discord.Embed(
                                    title="Ban",
                                    color=discord.Color.blue())
                            embed.add_field(name="Gebannte Person", value=args1.mention, inline=True)
                            embed.add_field(name="Gebannt von", value=message.author.mention, inline=True)
                            embed.add_field(name="Reason", value=reason, inline=False)
                            embed.set_thumbnail(url=target.avatar_url)
                            embed.timestamp = datetime.datetime.now()
                            await message.send(embed=embed)
                            await message.guild.ban(args1, reason=reason)
                            await message.send("Ban completed", delete_after=5)

                        if res.component.label == "Nein":
                            await message.send("Ban wurde abgebrochen")
                            await asyncio.sleep(3)
                            await message.channel.purge(limit=3)
                            return

                    if message.author.id == args1.id:
                        await message.send("Du kannst dich nicht selbst bannen")
                        return
                if not message.author.guild_permissions.ban_members :
                    await message.send("Du hast nicht genug **Berechtigungen** für diesen Command\n"
                                       "```Benötigte Permissions = Ban Members```")

            if language == "english":
                if message.author.guild_permissions.ban_members:
                    if not message.author.id == args1.id:
                        m = await message.send(f"Are you sure to ban {args1} for {reason}?",
                                               components=[button1])
                        res = await self.client.wait_for('button_click')
                        if res.component.label == "Yes":
                            await message.delete(m)
                            target = await self.client.fetch_user(args1.id)
                            dm = await target.create_dm()
                            embedm = discord.Embed(
                                title="Ban",
                                description=f"You got banned from {message.guild.name}",
                                color=discord.Color.red())
                            embedm.add_field(name="Banned by", value=message.author, inline=True)
                            embedm.add_field(name="Reason", value=reason, inline=True)
                            embedm.timestamp = datetime.datetime.now()
                            embedm.set_image(url=target.avatar_url)
                            await dm.send(embed=embedm)
                            embed = discord.Embed(
                                title="Ban",
                                color=discord.Color.blue())
                            embed.add_field(name="Banned Person", value=args1.mention, inline=True)
                            embed.add_field(name="Banned by", value=message.author.mention, inline=True)
                            embed.add_field(name="Reason", value=reason, inline=False)
                            embed.set_thumbnail(url=target.avatar_url)
                            embed.timestamp = datetime.datetime.now()
                            await message.send(embed=embed)
                            await message.guild.ban(args1, reason=reason)
                            await message.send("Ban completed", delete_after=5)

                        if res.component.label == "No":
                            await message.send("Ban stopped")
                            await asyncio.sleep(3)
                            await message.channel.purge(limit=3)
                            return
                    if message.author.id == args1.id:
                        await message.send("You can't ban yourself")
                        return
                if not message.author.guild_permissions.ban_members:
                    await message.send("You don't have enough **Permissions** to do that Command\n"
                                       "````Required Permissions = Ban Members```")

        @commands.command()
        async def kick(self, message, args1: discord.Member, *, reason):
            button1 = [[Button(style=ButtonStyle.green, label="Yes"), Button(style=ButtonStyle.red, label="No")]]
            button2 = [[Button(style=ButtonStyle.green, label="Ja"), Button(style=ButtonStyle.red, label="Nein")]]
            settings = await guild_settings.find_one({"_id": int(message.guild.id)})
            language = settings["settings"]["language"]
            team_id = settings["settings"]["team role"]
            if not team_id == "None":
                team_role = discord.utils.get(message.guild.roles, id=team_id)
                if language == "german":
                    if message.author.guild_permissions.kick_members or message.author in team_role.members:
                        m = await message.send(f"Bist du dir sicher das du {args1} kicken willst für {reason}?",
                                               components=[button2])
                        res = await self.client.wait_for('button_click')
                        if res.component.label == "Ja":
                            await message.delete(m)
                            target = await self.client.fetch_user(args1.id)
                            dm = await target.create_dm()
                            embedm = discord.Embed(
                                title="Kicked",
                                description=f"Du wurdest von {message.guild.name} gekicked",
                                color=discord.Color.red())
                            embedm.add_field(name="Kicked by", value=message.author, inline=True)
                            embedm.add_field(name="Reason", value=reason, inline=True)
                            embedm.timestamp = datetime.datetime.now()
                            embedm.set_image(url=target.avatar_url)
                            await dm.send(embed=embedm)
                            embed = discord.Embed(
                                title="Kicked",
                                color=discord.Color.blue())
                            embed.add_field(name="Kicked Person", value=args1.mention, inline=True)
                            embed.add_field(name="Kicked by", value=message.author.mention, inline=True)
                            embed.add_field(name="Reason", value=reason, inline=False)
                            embed.set_thumbnail(url=target.avatar_url)
                            embed.timestamp = datetime.datetime.now()
                            await message.send(embed=embed)
                            await message.guild.kick(args1, reason=reason)
                            await message.send("Kick completed", delete_after=5)
                        if res.component.label == "Nein":
                            await message.send("Kick wurde abgebrochen")
                            return

                        if message.author.id == args1.id:
                            await message.send("Du kannst dich nicht Selber kicken")
                            return
                    if message.author.guild_permissions.kick_members and not message.author in team_role.members:
                        await message.send("Du hast nicht genug **Berechtigungen** für diesen Command\n"
                                           "```Benötigte Permissions = Kick Members```")

                if language == "english":
                    if message.author.guild_permissions.kick_members or message.author in team_role.members:
                        m = await message.send(f"Are you sure to kick {args1} for {reason}?", components=[button1])
                        res = await self.client.wait_for('button_click')
                        if res.component.label == "Yes":
                            await message.delete(m)
                            target = await self.client.fetch_user(args1.id)
                            dm = await target.create_dm()
                            embedm = discord.Embed(
                                title="Kicked",
                                description=f"You got kicked from {message.guild.name}",
                                color=discord.Color.red())
                            embedm.add_field(name="Kicked by", value=message.author, inline=True)
                            embedm.add_field(name="Reason", value=reason, inline=True)
                            embedm.timestamp = datetime.datetime.now()
                            embedm.set_image(url=target.avatar_url)
                            await dm.send(embed=embedm)
                            embed = discord.Embed(
                                title="Kicked",
                                color=discord.Color.blue())
                            embed.add_field(name="Kicked Person", value=args1.mention, inline=True)
                            embed.add_field(name="Kicked by", value=message.author.mention, inline=True)
                            embed.add_field(name="Reason", value=reason, inline=False)
                            embed.set_thumbnail(url=target.avatar_url)
                            embed.timestamp = datetime.datetime.now()
                            await message.send(embed=embed)
                            await message.guild.kick(args1, reason=reason)
                            await message.send("Kick completed", delete_after=5)
                        if res.component.label == "No":
                            await message.send("Kick stopped")
                            return
                        if message.author.id == args1.id:
                            await message.send("You can't kick yourself")
                            return
                    if message.author.guild_permissions.kick_members and not message.author in team_role.members:
                        await message.send("You don't have enough **Permissons** for this Command\n"
                                           "```Required Permissions = Kick Members```")

            if team_id == "None":
                if language == "german":
                    if message.author.guild_permissions.kick_members:
                        m = await message.send(f"Bist du dir sicher das du {args1} kicken willst für {reason}?", components=[button2])
                        res = await self.client.wait_for('button_click')
                        if res.component.label == "Ja":
                            await message.delete(m)
                            target = await self.client.fetch_user(args1.id)
                            dm = await target.create_dm()
                            embedm = discord.Embed(
                                title="Kicked",
                                description=f"Du wurdest von {message.guild.name} gekicked",
                                color=discord.Color.red())
                            embedm.add_field(name="Kicked by", value=message.author, inline=True)
                            embedm.add_field(name="Reason", value=reason, inline=True)
                            embedm.timestamp = datetime.datetime.now()
                            embedm.set_image(url=target.avatar_url)
                            await dm.send(embed=embedm)
                            embed = discord.Embed(
                                title="Kicked",
                                color=discord.Color.blue())
                            embed.add_field(name="Kicked Person", value=args1.mention, inline=True)
                            embed.add_field(name="Kicked by", value=message.author.mention, inline=True)
                            embed.add_field(name="Reason", value=reason, inline=False)
                            embed.set_thumbnail(url=target.avatar_url)
                            embed.timestamp = datetime.datetime.now()
                            await message.send(embed=embed)
                            await message.guild.kick(args1, reason=reason)
                            await message.send("Kick completed", delete_after=5)
                        if res.component.label == "Nein":
                            await message.send("Kick wurde abgebrochen")
                            return
                        if message.author.id == args1.id:
                            await message.send("Du kannst dich nicht Selber kicken")
                            return
                    if message.author.guild_permissions.kick_members:
                        await message.send("Du hast nicht genug **Berechtigungen** für diesen Command\n"
                                           "```Benötigte Permissions = Kick Members```")

                if language == "english":
                    if message.author.guild_permissions.kick_members:
                        m = await message.send(f"Are you sure to kick {args1} for {reason}?", components=[button1])
                        res = await self.client.wait_for('button_click')
                        if res.component.label == "Yes":
                            await message.delete(m)
                            target = await self.client.fetch_user(args1.id)
                            dm = await target.create_dm()
                            embedm = discord.Embed(
                                title="Kicked",
                                description=f"You got kicked from {message.guild.name}",
                                color=discord.Color.red())
                            embedm.add_field(name="Kicked by", value=message.author, inline=True)
                            embedm.add_field(name="Reason", value=reason, inline=True)
                            embedm.timestamp = datetime.datetime.now()
                            embedm.set_image(url=target.avatar_url)
                            await dm.send(embed=embedm)
                            embed = discord.Embed(
                                title="Kicked",
                                color=discord.Color.blue())
                            embed.add_field(name="Kicked Person", value=args1.mention, inline=True)
                            embed.add_field(name="Kicked by", value=message.author.mention, inline=True)
                            embed.add_field(name="Reason", value=reason, inline=False)
                            embed.set_thumbnail(url=target.avatar_url)
                            embed.timestamp = datetime.datetime.now()
                            await message.send(embed=embed)
                            await message.guild.kick(args1, reason=reason)
                            await message.send("Kick completed", delete_after=5)
                        if res.component.label == "No":
                            await message.send("Kick stopped")
                            return
                        if message.author.id == args1.id:
                            await message.send("You can't kick yourself")
                            return
                    if message.author.guild_permissions.kick_members:
                        await message.send("You don't have enough **Permissons** for this Command\n"
                                           "```Required Permissions = Kick Members```")



    @commands.command()
    async def unban(self, message, args1: discord.User):
        button1 = [[Button(style=ButtonStyle.green, label="Yes"), Button(style=ButtonStyle.red, label="No")]]
        button2 = [[Button(style=ButtonStyle.green, label="Ja"), Button(style=ButtonStyle.red, label="Nein")]]
        language = data[str(message.guild.id)]["language"]
        team_id = data[str(message.guild.id)]["team role"]
        if not team_id == "None":
            team_role = discord.utils.get(message.guild.roles, id=team_id)
            if language == "german":
                if message.author.guild_permissions.ban_members or message.author in team_role.members:
                    res = await self.client.wait_for('button_click')
                    m = await message.send(f"Bist du dir sicher das du {args1.name} entbannen willst?", components=button2)
                    if res.component.label == "Ja":
                        await message.delete(m)
                        embed = discord.Embed(title="Unbanned", color=discord.Color.green())
                        embed.add_field(name="Unbanned Person", value=f"{args1.name} | {args1.id}", inline=True)
                        embed.add_field(name="Unbanned by", value=message.author.mention, inline=True)
                        await message.guild.unban(args1)
                        await message.send(embed=embed)
                    if res.component.label == "Nein":
                        await message.delete(m)
                        await message.send("Unbann wurde abgebrochen")
                    if message.author.id == args1.id:
                        await message.send("Du kannst dich nicht Selber entbannen, da du ja nicht gebannt bist :D")
                        return
                if not message.author.guild_permissions.ban_members and not message.author not in team_role.members:
                    await message.send("Du hast keine **Berechtigungen** für diesen Command\n"
                                       "```Benötigte Berechtigungen = Ban Members```")
            if language == "english":
                if message.author.guild_permissions.ban_members or message.author in team_role.members:
                    res = await self.client.wait_for('button_click')
                    m = await message.send(f"Are you sure to unbann {args1.name}?", components=button1)
                    if res.component.label == "Yes":
                        await message.delete(m)
                        embed = discord.Embed(title="Unbanned", color=discord.Color.green())
                        embed.add_field(name="Unbanned Person", value=f"{args1.name} | {args1.id}", inline=True)
                        embed.add_field(name="Unbanned by", value=message.author.mention, inline=True)
                        await message.guild.unban(args1)
                        await message.send(embed=embed)
                    if res.component.label == "No":
                        await message.delete(m)
                        await message.send("Unbann stopped")
                    if message.author.id == args1.id:
                        await message.send("You can't unbann yourself, because you aren't banned :D")
                        return
                if not message.author.guild_permissions.ban_members and not message.author not in team_role.members:
                    await message.send("You don't have enough **Permissions** to do that Command\n"
                                       "````Required Permissions = Ban Members```")

        if team_id == "None":
            if language == "german":
                if message.author.guild_permissions.ban_members:
                    res = await self.client.wait_for('button_click')
                    m = await message.send(f"Bist du dir sicher das du {args1.name} entbannen willst?", components=button2)
                    if res.component.label == "Ja":
                        await message.delete(m)
                        embed = discord.Embed(title="Unbanned", color=discord.Color.green())
                        embed.add_field(name="Unbanned Person", value=f"{args1.name} | {args1.id}", inline=True)
                        embed.add_field(name="Unbanned by", value=message.author.mention, inline=True)
                        await message.guild.unban(args1)
                        await message.send(embed=embed)
                    if res.component.label == "Nein":
                        await message.delete(m)
                        await message.send("Unbann wurde abgebrochen")
                    if message.author.id == args1.id:
                        await message.send("Du kannst dich nicht Selber entbannen, da du ja nicht gebannt bist :D")
                        return
                if not message.author.guild_permissions.ban_members:
                    await message.send("Du hast keine **Berechtigungen** für diesen Command\n"
                                       "```Benötigte Berechtigungen = Ban Members```")

            if language == "english":
                if message.author.guild_permissions.ban_members:
                    res = await self.client.wait_for('button_click')
                    m = await message.send(f"Are you sure to unbann {args1.name}?", components=button1)
                    if res.component.label == "Yes":
                        await message.delete(m)
                        embed = discord.Embed(title="Unbanned", color=discord.Color.green())
                        embed.add_field(name="Unbanned Person", value=f"{args1.name} | {args1.id}", inline=True)
                        embed.add_field(name="Unbanned by", value=message.author.mention, inline=True)
                        await message.guild.unban(args1)
                        await message.send(embed=embed)
                    if res.component.label == "No":
                        await message.delete(m)
                        await message.send("Unbann stopped")
                    if message.author.id == args1.id:
                        await message.send("You can't unbann yourself, because you aren't banned :D")
                        return
                if not message.author.guild_permissions.ban_members:
                    await message.send("You don't have enough **Permissions** to do that Command\n"
                                       "````Required Permissions = Ban Members```")

def setup(client):
    client.add_cog(Cogs(client))
