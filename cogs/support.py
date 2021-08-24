import discord
from discord.ext import commands
import datetime
import json
from discord_components import (
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)

with open("./config.json", "r") as config:
    config = json.load(config)


class Support(commands.Cog, description=f"Support for the Bot"):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.dev_only = False


    @commands.command(help="If you find a Bug you can report it with this command")
    async def bug(self, ctx, *, args):
        invite = await ctx.channel.create_invite(max_age=172800)
        embed = discord.Embed(
            title="Bug",
            description="Are you Sure you want to report this Bug abusing this could blacklist you from using this Bot",
            color=int(config["colors"]["Main"]))
        buttons = [[Button(style=ButtonStyle.green, label="Yes"), Button(style=ButtonStyle.red, label="No")]]
        await ctx.send(embed=embed, components=buttons)
        res = await self.client.wait_for('button_click')
        if res.component.label == "Yes":
            channel = self.client.get_channel(879148087954792488)
            await res.send(content="Send")
            embed = discord.Embed(title="Bug Report", color=int(config["colors"]["Main"]))
            embed.add_field(name="Report from", value=f"{ctx.author.name} | {ctx.author.id}", inline=True)
            embed.add_field(name="Time", value=f"<t:{round(datetime.datetime.now().timestamp())}>", inline=True)
            if ctx.channel.type is not discord.ChannelType.private:
                embed.add_field(name="From Guild", value=f"[{ctx.guild.name}]({invite}) | {ctx.guild.id}", inline=True)
            embed.add_field(name="Bug Explaination", value=f"{args}", inline=False)
            await channel.send(embed=embed)
        if res.component.label == "No":
            await res.send(content="Stopped the Report")
            return

    @commands.command(help="If you have a suggestion you can tell us that with this command")
    async def suggestion(self, ctx, *, args):
        invite = await ctx.channel.create_invite(max_age=172800)
        embed = discord.Embed(
            title="Suggestion",
            description="Are you Sure you want to suggest this? abusing this could blacklist you from using this Bot",
            color=int(config["colors"]["Main"]))
        buttons = [[Button(style=ButtonStyle.green, label="Yes"), Button(style=ButtonStyle.red, label="No")]]
        await ctx.send(embed=embed, components=buttons)
        res = await self.client.wait_for('button_click')
        if res.component.label == "Yes":
            channel = self.client.get_channel(879155519430991922)
            await res.send(content="Send")
            embed = discord.Embed(title="Suggestion", color=int(config["colors"]["Main"]))
            embed.add_field(name="Suggestion from", value=f"{ctx.author.name} | {ctx.author.id}", inline=True)
            embed.add_field(name="Time", value=f"<t:{round(datetime.datetime.now().timestamp())}>", inline=True)
            if ctx.channel.type is not discord.ChannelType.private:
                embed.add_field(name="From Guild", value=f"[{ctx.guild.name}]({invite}) | {ctx.guild.id}", inline=True)
            embed.add_field(name="Suggestion", value=f"{args}", inline=False)
            await channel.send(embed=embed)
        if res.component.label == "No":
            await res.send(content="Stopped the Suggestion")
            return




def setup(client):
    client.add_cog(Support(client))