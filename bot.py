# bot.py
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


# when the bot is connected
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


# on received message in channel
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '.b':
        # some hypothetical balance from a db
        # reported to the user
        await message.author.send('👋')
        await message.author.send(f"Your Balance is ... | {message.author}")


client.run(TOKEN)
