import discord
from discord.ext import commands
import os

TOKEN = os.environ['TOKEN']

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.content.startswith('rat'):
            await message.channel.send('Eeek!')
        if message.author.voice:
            channel = message.author.voice.channel
            await channel.connect()

client = MyClient()
client.run(TOKEN)
