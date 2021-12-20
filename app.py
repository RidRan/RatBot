import discord
from discord.ext import commands
import os

TOKEN = os.environ['TOKEN']

NOISE = 'scream.mp3'

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
            reply = 'Name: ' + message.author.name
            await message.channel.send(reply)
            if message.author.voice:
                channel = message.author.voice.channel

                await message.channel.send('Joining ' + message.author.name + ' in ' + channel.name)

                voices = self.voice_clients
                voice = None
                for v in voices:
                    if v.guild.id == message.guild.id:
                        voice = v

                if voice and voice.is_connected():
                    await voice.move_to(channel)
                else:
                    voice = await channel.connect()
                audio = discord.FFmpegPCMAudio(NOISE)
                print('Playing' + NOISE)
                voice.play(audio, after=None)
                voice.disconnect()

            else:
                await message.channel.send(message.author.name + ' is not in a channel')

client = MyClient()
client.run(TOKEN)
