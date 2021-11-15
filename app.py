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
            reply = 'Nick: ' + message.author.name
            await message.channel.send(reply)
            if message.author.voice:
                await message.channel.send('Joining ' + message.author.name)
                channel = message.author.voice.channel
                await channel.connect()
            else:
                await message.channel.send(message.author.name + ' is not in a channel')

client = MyClient()
client.run(TOKEN)
