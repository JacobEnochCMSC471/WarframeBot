import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("API_KEY")

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def on_ready(self):
    print(f'Logged on as {self.user}!')


@client.event
async def on_message(message):
    if message.author.bot:  # Do not respond to other bots
        return

    if message.author.id in [client.user.id]:  # Prevent infinite spamming by responding to itself
        return

    print(f'Message from {message.author}: {message.content}')
    return

def main():
    client.run(token)


main()
