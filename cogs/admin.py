import asyncio
import logging
import random
import discord
from discord.ext import commands, tasks
import json


with open("./config.json", "r") as config:
    config = json.load(config)

giveaway_users = []


def convert(date):
    pos = ["s", "m", "h", "d"]
    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}
    i = {"s": "Seconds", "m": "Minutes", "h": "Hours", "d": "Days"}
    unit = date[-1]
    if unit not in pos:
        return -1
    try:
        val = int(date[:-1])

    except ValueError:
        return -2

    if val == 1:
        return val * time_dic[unit], i[unit][:-1]
    else:
        return val * time_dic[unit], i[unit]

class admin(commands.Cog, description=f"Commands for Administrator from a Server"):
    def __init__(self, client):
        self.client = client
        self.hidden = False
        self.dev_only = False




def setup(client):
    client.add_cog(admin(client))