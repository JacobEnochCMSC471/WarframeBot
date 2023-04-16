import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import logging
from pymongo import MongoClient
import utility

load_dotenv()
token = os.getenv("API_KEY")
guild_id = os.getenv("GUILD_KEY")
intents = discord.Intents.all()

try:
    db_client = MongoClient("mongodb://localhost:27017/")
    relic_db = db_client['WarframeRelics']

    axi_collection = relic_db.get_collection("Axi")
    neo_collection = relic_db.get_collection("Neo")
    meso_collection = relic_db.get_collection("Meso")
    lith_collection = relic_db.get_collection("Lith")

except:
    print(
        "Database likely not connected or configured correctly. Please modify connection settings or make sure you have MongoDB and a server running with the required data.")
    exit(0)


class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False  # added to make sure that the command tree will be synced only once
        self.added = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            await tree.sync(guild=discord.Object(guild_id))
            self.synced = True
        if not self.added:
            self.added = True


client = Client()
tree = app_commands.CommandTree(client)


@tree.command(name="relic_request", guild=discord.Object(guild_id), description="Look up what relics are needed for primed items!")
async def relic_request(interaction: discord.Interaction, item: str):
    # Make sure that the entered text only consists of characters
    if all(x.isalpha() or x.isspace() for x in item):
        userQuery = {'rewards.Intact.itemName': item}
        axiQueryResult = axi_collection.find(userQuery)
        neoQueryResult = neo_collection.find(userQuery)
        mesoQueryResult = meso_collection.find(userQuery)
        lithQueryResult = lith_collection.find(userQuery)

        combinedQueries = [axiQueryResult, neoQueryResult, mesoQueryResult, lithQueryResult]
        relicList = []

        for queryResult in combinedQueries:
            for indvResult in queryResult:
                itemIndex = utility.search_list(indvResult['rewards']['Intact'], item)
                tempItemName = indvResult['rewards']['Intact'][itemIndex]['itemName']
                tempTier = indvResult['tier']
                tempName = indvResult['name']

                relicList.append({'tier': tempTier, 'name': tempName, 'itemName': tempItemName})

        botRelicResponse = '-----Relics Needed For {}-----\n'.format(relicList[0]['itemName'])

        for item in relicList:
            relicText = "{} {}\n".format(item['tier'], item['name'])
            botRelicResponse += relicText

        await interaction.response.send_message(botRelicResponse)

    else:
        await interaction.response.send_message("{}, please enter a sequence of letters only.".format(interaction.user.mention))
        return


@client.event
async def on_message(message):
    if message.author == client.user:
        return


@client.event
async def on_command_error(ctx, error):
    pass


def main():
    client.run(token)


main()
