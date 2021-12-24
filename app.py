import discord
from discord.ext import commands
import os
import time

TOKEN = os.environ['TOKEN']

NOISE = 'scream.mp3'


class MyClient(discord.Client):
    init = False

    async def on_ready(self):
        print('Logged in as ' + self.user.name + ' (' + str(self.user.id) + ')')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.content.startswith('rat_init'):
            # reply = 'Name: ' + message.author.name
            # await message.channel.send(reply)

            if self.init == False:
                self.init = True

                if message.author.voice:
                    channel = message.author.voice.channel

                    # await message.channel.send('Joining ' + message.author.name + ' in ' + channel.name)

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
                    while voice.is_playing():
                        pass 
                    await voice.disconnect()

                else:
                    await message.channel.send(message.author.name + ' is not in a channel')
            else:
                await message.channel.send('The Rat is already awake')

client = MyClient()
client.run(TOKEN)
