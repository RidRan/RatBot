import discord
from discord.ext import commands
import os

TOKEN = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_message(message):
#     if message.author.voice:
#         channel = message.author.voice.channel
#         await channel.connect()
#     else:
#         await client.send_message(message.channel, "Not in channel")
      await client.send_message(message.channel, message.content)
        
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
