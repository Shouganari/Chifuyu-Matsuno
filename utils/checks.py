from discord.ext import commands
import json

with open("./config.json", "r") as config:
    config = json.load(config)


def is_dev():
    async def pred(ctx):
        if ctx.author.id in config["devs"]:
            return True

    return commands.check(pred)


