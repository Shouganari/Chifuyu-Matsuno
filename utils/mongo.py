import motor.motor_asyncio
import json

with open("./config.json", "r") as config:
    config = json.load(config)

cluster = config["db"]["cluster"]

cluster = motor.motor_asyncio.AsyncIOMotorClient(
    cluster)

db = cluster["Chifuyu"]

settings = db["settings"]

blacklist = db["blacklist"]

#users = db["user"]

#warnings = db["warnings"]

