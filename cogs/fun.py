import discord
from discord.ext import commands
import asyncio
import json
import datetime
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption)
import random
with open("./config.json", "r") as config:
    config = json.load(config)



class fun(commands.Cog, description="Fun Commands"):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.dev_only = False

    @commands.command(help="Get a Topic over that you can Talk")
    @commands.guild_only()
    async def topic(self, ctx):
        topics = ["Do you have any hoobies?", "What is your favorite sport?", "What is your favorite video game",
                  "What's your favorite content creator?", "Do you have a crush, if so what is his / her name?",
                  "What is your favorite fashion style?", "What is your favorite school subject?",
                  "What is your favorite movie?",
                  "Xbox or Playstation?", "Do you watch anime, if so what is your favorite anime?",
                  "Who is your favorite character?", "Do you read books and if so what is your favorite book?",
                  "Are you religious?", "What is your star sign?", "When is your birthday?",
                  "Are you a content creator",
                  "What's your favorite song ", "Who is your favorite singer / rapper",
                  "What is your favorite music genre?",
                  "What is your favorite movie genre?", "What is your favorite drink?", "What is your favorite food",
                  "Who is your favorite server member?", "Do you play ** Clash Royale **, if so which arena are you?",
                  "What country were you born in?", "Do you have a pet?", "Who is a favorite team member?",
                  "What / who inspires you?", "Do you have a dream job or are you already working your dream job",
                  "If you could know the answer to one question about your future, what would the question be?",
                  "How much time do you spend on the internet? What do you usually do?",
                  "Do you wish for more or less holidays? and Why?",
                  "If you opened a restaurant what kind of food would you serve?", "What are you obsessed with?",
                  "What's the best thing about a cold winter day?", "What's the weirdest app you've heard of or tried?",
                  "Are there any songs that always make you cry?", "What are app creator doing that really annoys you?",
                  "What problems will the technology solve in the next 5 years? What problems will it cause?",
                  "Who is the most interesting person you follow? ",
                  " Do you cry while watching movies / series / anime?",
                  "If you're a content creator, what kind of content do you do?"]
        embed = discord.Embed(title="Topic", color=int(config["colors"]["Main"]), description=f"Your topic is:\n\r**{random.choice(topics)}**")
        await ctx.send(embed=embed)

    @commands.command(help="Get a Random answer")
    async def question(self, ctx, *, args):
        answer = ["Yes", "No", "Maybe"]
        await ctx.send(f"The answer to you question `{args}` is {random.choice(answer)}")





def setup(client):
    client.add_cog(fun(client))