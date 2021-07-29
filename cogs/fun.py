import discord
from discord.ext import commands
import datetime
import random
from utils.mongo import cluster, db, guild_settings

class Cogs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def avatar(self, message, args1: discord.Member):
        embed = discord.Embed(title=f"{args1.name}'s Avatar", color=discord.Color.blue())
        embed.timestamp = datetime.datetime.now()
        embed.set_image(url=args1.avatar_url)
        await message.send(embed=embed)

    @commands.command(aliases=["topic"])
    async def thema(self, message):
        settings = await guild_settings.find_one({"_id": int(message.guild.id)})
        language = settings["settings"]["language"]
        if language == "german":
            de = ["Hast du irgendwelche Hoobies?", "Was ist deine Lieblings Sportart?",
                  "Was ist dein Lieblings Videospiel",
                  "Was ist dein Lieblings Content Creator?", "Hast du einen Crush, wenn ja was ist sein/ihr Name?",
                  "Was ist dein Lieblings Mode Style?", "Was ist dein Lieblings Schulfach?",
                  "Was ist dein Lieblings Film?",
                  "Xbox oder Playstation?", "Schaust du Anime, wenn ja was ist dein Lieblings Anime?",
                  "Wer ist dein Lieblings Charakter?", "Liest du Bücher, und wenn ja was ist dein Lieblings Buch?",
                  "Bist du Gläubig?", "Was ist dein Sternzeichen?", "Wann hast du Geburtstag?",
                  "Bist du selbst ein Content Creator?",
                  "Was ist dein Lieblingslied", "Wer ist dein Lieblings Sänger/Rapper",
                  "Was ist deine Lieblings Musik Genre?",
                  "Was ist deine Lieblings Film Genre?", "Was ist dein Lieblingsgetränk?",
                  "Was ist dein Lieblingsessen?",
                  "Wer ist dein Lieblings Server Mitglied?",
                  "Spielst du **Clash Royale**, wenn ja welche Arena bist du?",
                  "In welchem Land wurdest du geboren?", "Hast du ein Haustier?",
                  "Wer ist ein Lieblings Team Mitglied?",
                  "Was/Wer inspiriert dich?", "Hast du einen Traumberuf oder arbeitest du schon deinen Traumberuf",
                  "Wenn du die Antwort auf eine Frage zu deiner Zukunft erfahren könnten, welche wäre die Frage?",
                  "Wie viel Zeit verbringst du im Internet? Was machst du normalerweise?",
                  "Wünschst du dir mehr oder weniger Feiertage? Warum?",
                  "Wenn du ein Restaurant eröffnen würdest, welche Art von Essen würdest du servieren?",
                  "Wovon bist du besessen?", "Was ist das Beste an einem kalten Wintertag?",
                  "Was ist die seltsamste App, von der du gehört oder die du ausprobiert hast?",
                  "Gibt es Songs, die dich immer zum weinen bringen?",
                  "Was machen App-Hersteller, das dich wirklich nervt?",
                  "Welche Probleme wird die Technologie in den nächsten 5 Jahren lösen? Welche Probleme wird es verursachen?",
                  "Wer ist die interessanteste Person, der du folgst?", "Weinst du bei Filmen/Serien/Anime?",
                  "Wenn du ein Content Creator bist, was machst du so für Content?"]
            embed = discord.Embed(title="Thema", color=discord.Color.blue(), description=f"\n\r"
                                                                                         f"{random.choice(de)}")
            await message.send(embed=embed)
        if language == "english":
            en = ["Do you have any hoobies?", "What is your favorite sport?", "What is your favorite video game",
                  "What's your favorite content creator?", "Do you have a crush, if so what is his / her name?",
                  "What is your favorite fashion style?", "What is your favorite school subject?",
                  "What is your favorite movie?",
                  "Xbox or Playstation?", "Do you watch anime, if so what is your favorite anime?",
                  "Who is your favorite character?", "Do you read books and if so what is your favorite book?",
                  "Are you religious?", "What is your star sign?", "When is your birthday?",
                  "Are you a content creator",
                  "What's your favorite song ", " Who is your favorite singer / rapper",
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
            embed = discord.Embed(title="Topic", color=discord.Color.blue(), description=f"\n\r"
                                                                                         f"{random.choice(en)}")
            await message.send(embed=embed)


def setup(client):
    client.add_cog(Cogs(client))
