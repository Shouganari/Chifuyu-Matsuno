from discord.ext import commands
from discord.ext import commands

from utils.emoji import error_emoji
from utils.mongo import guild_settings


class Error(commands.Cog, name="Error"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, message, error):
        settings = await guild_settings.find_one({"_id": int(message.guild.id)})
        language = settings["settings"]["language"]
        if isinstance(error, commands.CommandNotFound):
            if message.guild is None:
                await message.send(f"This command doesn't exist {error_emoji}")
            if message.guild is not None:
                if language == "german":
                    await message.send(f"Diesen Command gibt es nicht {error_emoji}")
                if language == "english":
                    await message.send(f"This command doesn't exist {error_emoji}")
        if isinstance(error, commands.MissingPermissions):
            if language == "german":
                await message.send(f"Du hast nicht genung Permissions für diesen Command {error_emoji}")
            if language == "english":
                await message.send(f"You don't have enough Permissions to do this Command {error_emoji}")

def setup(client):
    client.add_cog(Error(client))
