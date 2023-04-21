import discord
from discord import app_commands
import os
from dotenv import load_dotenv
import logging
from pymongo import MongoClient
from pymongo import errors
import utility

# Necessary stuff that needs to be loaded in before anything can be
load_dotenv()
token = os.getenv("API_KEY")
guild_id = os.getenv("GUILD_KEY")
intents = discord.Intents.all()

try:
    db_client = MongoClient("mongodb://localhost:27017/")
    relic_db = db_client['WarframeRelics']
    relic_collections = utility.populate_collections_list(relic_db)

except errors.ConnectionFailure:
    print(
        "Database likely not connected or configured correctly. Please modify connection settings or make sure you have MongoDB and a server running with the required data.")
    exit(0)

except errors.PyMongoError as generic_error:
    print('Some other PyMongo error occurred, see printed text for details.')
    print(generic_error)
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
    # Make sure that the entered text only consists of characters or spaces

    if all(char.isalpha() or char.isspace() for char in item):
        query_results = utility.get_user_query(item, relic_collections)

        await interaction.response.send_message(query_results)

    else:
        await interaction.response.send_message("{}, please enter a sequence of letters only.".format(interaction.user.mention))
        return

    return 0


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
