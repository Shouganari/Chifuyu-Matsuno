import asyncio
import datetime
import json
import logging
import os
import random
import shutil
import string

import Augmentor
import discord
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from discord.ext import commands

from utils.mongo import settings

with open("./config.json", "r") as config:
    config = json.load(config)


class captcha(commands.Cog, description="A Captcha"):
    def __init__(self, client):
        self.client = client
        self.hidden = True
        self.dev_only = False

    @commands.Cog.listener()
    async def on_member_join(self, member):
        protection = await settings.find_one({"_id": int(member.guild.id)})
        captcha_log = protection["protection"]["log-channel"]
        if member.bot:
            return
        minAccountdate = protection["protection"]["min-Account-Date"]
        if minAccountdate is not False:
            userAccountDate = member.created_at.timestamp()
            if userAccountDate < minAccountdate:
                embed = discord.Embed(title=f"You got kicked from {member.guild.name}",
                                      description=f"You got kicked because your Account is too young you account need to be older than {minAccountdate}",
                                      color=int(config["colors"]["error"]))
                try:
                    await member.send(embed=embed)
                except Exception as e:
                    pass
                await member.kick()
                if protection["protection"]["log-channel"] is not False:
                    log_channel = self.client.get_channel(int(protection["protection"]["log-channel"]))
                    embed = discord.Embed(title="Member Kicked", color=int(config["colors"]["error"]))
                    embed.add_field(name="Reason", value=f"The Account was too young:\n <t:{userAccountDate}:F>",
                                    inline=True)
                    embed.add_field(name="Time", value=f"<t:{datetime.datetime.now()}:F>")
                    await log_channel.send(embed=embed)
        if protection["protection"]["captcha"]["status"] is True and protection["protection"]["captcha"]["channel"] is not False and protection["protection"]["captcha"]["role"] is not False:
            memberTime = f"{member.joined_at.year}-{member.joined_at.month}-{member.joined_at.day} {member.joined_at.hour}:{member.joined_at.minute}:{member.joined_at.second}"
            captcha = await settings.find_one({"_id": int(member.guild.id)})
            image = np.zeros(shape=(100, 350, 3), dtype=np.uint8)

            image = Image.fromarray(image + 255)

            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(font="./locales/fonts/Roboto-Black.ttf", size=60)

            text = ' '.join(
                random.choice(string.ascii_uppercase) for _ in range(6))

            W, H = (350, 100)
            w, h = draw.textsize(text, font=font)
            draw.text(((W - w) / 2, (H - h) / 2), text, font=font, fill=(90, 90, 90))

            ID = member.id
            folderPath = f"locales/img/captchaFolder/captcha_{ID}"
            try:
                os.mkdir(folderPath)
            except:
                if os.path.isdir('locales/img/captchaFolder') is False:
                    os.mkdir("locales/img/captchaFolder")
                if os.path.isdir(folderPath) is True:
                    shutil.rmtree(folderPath)
                os.mkdir(folderPath)
            image.save(f"{folderPath}/captcha{ID}.png")

            p = Augmentor.Pipeline(folderPath)
            p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=14)
            p.process()

            path = f"{folderPath}/output"
            files = os.listdir(path)
            captchaName = [i for i in files if i.endswith('.png')]
            captchaName = captchaName[0]

            image = Image.open(f"{folderPath}/output/{captchaName}")

            width = random.randrange(6, 8)
            co1 = random.randrange(0, 75)
            co3 = random.randrange(275, 350)
            co2 = random.randrange(40, 65)
            co4 = random.randrange(40, 65)
            draw = ImageDraw.Draw(image)
            draw.line([(co1, co2), (co3, co4)], width=width, fill=(90, 90, 90))

            noisePercentage = 0.25

            pixels = image.load()
            for i in range(image.size[0]):
                for j in range(image.size[1]):
                    rdn = random.random()
                    if rdn < noisePercentage:
                        pixels[i, j] = (90, 90, 90)

            image.save(f"{folderPath}/output/{captchaName}_2.png")

            captchaFile = discord.File(f"{folderPath}/output/{captchaName}_2.png")

            tries = 3



            channel = self.client.get_channel(int(captcha["protection"]["captcha"]["channel"]))
            captcha_embed = await channel.send(
                f"**YOU MUST PASS THE CAPTCHA TO ENTER IN THE SERVER :**\nPlease {member.mention}, enter the captcha to get access to the whole serveur (only 6 uppercase letters).",
                file=captchaFile)

            while tries > 0:

                def check(m):
                    if m.author.id == member.id and m.content != "":
                        return m.content

                try:
                    msg = await self.client.wait_for('message', timeout=120.0, check=check)

                    password = text.split(" ")
                    password = "".join(password)
                    if msg.content == password:
                        embed = discord.Embed(description=f"{member.mention} passed the captcha.",
                                              color=discord.Color.green())
                        await channel.send(embed=embed)
                        try:
                            role = discord.utils.get(member.guild.roles, id=int(captcha["captcha"]["role"]))
                            await member.add_roles(role)
                        except Exception as error:
                            logging.error(f"Give and remove roles failed : {error}")
                        if captcha_log is not False:
                            channel = self.client.get_channel(int(captcha_log))
                            embed = discord.Embed(description=f"{member.name} passed the captcha.",
                                                  color=discord.Color.green())
                            await channel.send(embed=embed)
                        return
                    if msg.content != password:
                        if tries == 1:
                            tries -= 1
                            tries += 3
                            embed = discord.Embed(
                                description=f"{member.name} failed the captcha.\n You have no more tries. You have 1 More Try if you fail the captcha now you get kicked",
                                color=discord.Color.red())
                            await channel.send(embed=embed)
                            if captcha["protection"]["log-channel"] is not False:
                                logchannel = self.client.get_channel(int(captcha["protection"]["log-channel"]))
                                embed = discord.Embed(title=f"Captcha got Failed by {member.name}", color=discord.Color.red(), description=f"{member.name} got Kicked because he failed the Captcha 3 Times")
                                await logchannel.send(embed=embed)
                            await member.kick(reason="Failed the captcha")
                            return
                        if tries != 1:
                            embed = discord.Embed(
                                description=f"{member.name} failed the captcha.\n You have **{tries}** more tries.",
                                color=discord.Color.red())
                            await channel.send(embed=embed)
                            tries -= 1



                except asyncio.TimeoutError:
                    embed = discord.Embed(title=f"**TIME IS OUT**",
                                          description=f"{member.mention} has exceeded the response time (120s).",
                                          color=0xff0000)
                    await channel.send(embed=embed, delete_after=5)
                    try:
                        link = await channel.create_invite(max_age=172800)
                        embed = discord.Embed(title=f"**YOU HAVE BEEN KICKED FROM {member.guild.name}**",
                                              description=f"Reason : You exceeded the captcha response time (120s).\nServer link : <{link}>",
                                              color=0xff0000)
                        await member.send(embed=embed)
                        await member.kick(
                            reason="Reason : He exceeded the captcha response time (120s).\n\nUser informations :\n\nName : {member}\nId : {member.id}")
                    except Exception as error:
                        print(f"Log failed (onJoin) : {error}")
                    await asyncio.sleep(3)
                    await captcha_embed.delete()

                    if captcha_log is not False:
                        channel = self.client.get_channel(int(captcha_log))
                        embed = discord.Embed(title=f"**{member} has been kicked.**",
                                              description=f"**Reason :** He exceeded the captcha response time (120s).\n\n**__User informations :__**\n\n**Name :** {member}\n**Id :** {member.id}",
                                              color=0xff0000)
                        embed.set_footer(text=f"at {memberTime}")
                        await channel.send(embed=embed)

            try:
                await asyncio.sleep(5)
                shutil.rmtree(folderPath)
            except Exception as error:
                print(f"Delete captcha file failed {error}")


def setup(client):
    client.add_cog(captcha(client))
