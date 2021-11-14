import discord
from discord.ext import commands
import os

TOKEN = os.eviron['TOKEN']

client = discord.Client()

@client.event
async def on_message(message):
    if message.author.voice:
        channel = message.author.voice.channel
        await channel.connect()
    else:
        await client.send_message(message.channel, "Not in channel")

client.run(TOKEN)
