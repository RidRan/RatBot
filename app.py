import discord
from discord.ext import commands
import os
import asyncio

from discord.gateway import VoiceKeepAliveHandler

TOKEN = os.environ['TOKEN']

NOISE = 'scream.mp3'

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged in as ' + self.user.name + ' (' + str(self.user.id) + ')')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.content.startswith('rat'):
            while True:
                for channel in message.guild.voice_channels:
                    if len(channel.members) == 0:
                        for r in channel.changed_roles:
                            print(r.name)

                        voices = self.voice_clients
                        voice = None
                        for v in voices:
                            if v.guild.id == message.guild.id:
                                voice = v

                        if voice and voice.is_connected():
                            await voice.move_to(channel)
                        else:
                            voice = await channel.connect()

                        print('Joined ' + channel.name + ' (' + str(len(channel.members)) + ' members) in ' + channel.guild.name)

                        while len(channel.members) <= 1:
                            await asyncio.sleep(1)

                        audio = discord.FFmpegPCMAudio(NOISE)
                        print('Playing' + NOISE)
                        voice.play(audio, after=None)

                        while voice.is_playing():
                            await asyncio.sleep(1) 

                        await voice.disconnect()
                        print('Spooked by ' + voice.channel.members[0].name)
                        await message.channel.send('Spooked by ' + voice.channel.members[0].name)

                    else:
                        print(channel.name + ' is not empty')
                await asyncio.sleep(1800)

client = MyClient()
client.run(TOKEN)
