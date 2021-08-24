import datetime
import sys
import os
import random
import discord
import asyncio
import aiohttp
from discord.ext import commands
import json

from utils import checks
from utils.mongo import blacklist

with open("./config.json", "r") as config:
    config = json.load(config)


async def add_to_blacklist(object_id, reason):
    try:
        blacklist_check = await blacklist.find_one({"_id": int(object_id)})
        if int(object_id) != blacklist_check:
            await blacklist.insert_one({"_id": int(object_id), "reason": str(reason)})
    except Exception:
        pass


async def remove_from_blacklist(object_id):
    try:
        blacklist_check = await blacklist.find_one({"_id": int(object_id)})
        if int(object_id) == blacklist_check:
            blacklist.delete_one({"_id": int(object_id)})
        else:
            pass
    except Exception:
        pass

error = config["colors"]["error"]
class developer(commands.Cog, description=f"Commands for Developers of the bot"):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.dev_only = True

    @commands.command(help="Adds a User to the blacklist")
    @checks.is_dev()
    async def blacklist_add(self, ctx, args1, *, reason=None):
        await add_to_blacklist(object_id=args1, reason=reason)
        await ctx.reply(f"{args1} got blacklisted for {reason}", mention_author=False)

    @commands.command(help="Removes a User from the blacklist")
    @checks.is_dev()
    async def blacklist_remove(self, ctx, args1):
        await remove_from_blacklist(object_id=args1)
        await ctx.reply(f"{args1} got removed from the blacklist", mention_author=False)

    @commands.command(help="Stops the bot")
    @checks.is_dev()
    async def stop(self, ctx):
        await ctx.reply("Im Stopping ...", mention_author=False)
        await self.client.stop()
        sys.exit(0)

    @commands.command(help="Shows all Guilds on that the Bot is on", aliases=["all_guilds"])
    @checks.is_dev()
    async def all_servers(self, ctx):
        msg = '```js\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.client.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.send(msg)


    @commands.command(help="Leaves a guild")
    @checks.is_dev()
    async def leaveserver(self, ctx, guildid: str):
        if guildid == 'this':
            await ctx.guild.leave()
            return
        else:
            guild = self.client.get_guild(guildid)
            if guild:
                await guild.leave()
                msg = f"I left {guild.name}"
            else:
                msg = f"{error} Couldn't find this guild"
        await ctx.send(msg)

    @commands.command(help="Changes the Nickname from a Bot")
    @commands.bot_has_permissions(manage_nicknames=True)
    @checks.is_dev()
    async def nickname(self, ctx, *name):
        nickname = ' '.join(name)
        await ctx.me.edit(nick=nickname)
        if nickname:
            msg = f'Changing my nickname to **{nickname}**'
        else:
            msg = f'{error} Reset my server nickname to **{ctx.me.name}**'
        await ctx.send(msg)

    @commands.command(help="Sets the Nickname from a bot to")
    @commands.bot_has_permissions(manage_nicknames=True)
    @checks.is_dev()
    async def setnickname(self, ctx, member: discord.Member = None, *name):
        if member == None:
            member = ctx.author
        nickname = ' '.join(name)
        await member.edit(nick=nickname)
        if nickname:
            msg = f'Changing my Nickname from {member} to **{nickname}**'
        else:
            msg = f'Resets my Nickname from {member} to **{member.name}**'
        await ctx.send(msg)

    @commands.command(help="Gets a Server invite from a Server")
    @checks.is_dev()
    async def geninvite(self, ctx, serverid: str):
        guild = self.client.get_guild(int(serverid))
        invite = await self.client.create_invite(guild, max_uses=1, unique=False)
        msg = f'Invite for **{guild.name}** ({guild.id})\n{invite.url}'
        await ctx.author.send(msg)

    @commands.command(help="Send a Bot Announcment")
    @commands.is_owner()
    async def announcment(self, ctx):
        embed = discord.Embed(title=f"What Should be the announcment ?", color=int(config["colors"]["Main"]))
        await ctx.send(embed=embed)
        def check(m):
            if m.channel == ctx.channel and m.author == ctx.author:
                return m.content
        msg = await self.client.wait_for('message', timeout=300.0, check=check)
        with open("./news.json", "r") as f:
            news = json.load(f)

        news["time"] = datetime.datetime.now().strftime("%a %b - %B %Y")
        news["news"] = msg.content
        with open("./news.json", "w") as f:
            json.dump(news, f)
        await ctx.send("Announcment got send!")


def setup(client):
    client.add_cog(developer(client))
