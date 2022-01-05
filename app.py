import discord
from discord.ext import commands
import os
import time

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
        if message.content.startswith('member_test'):
            if message.author.voice:
                for m in message.author.voice.channel.members:
                    await message.channel.send(m.name)
        if message.content.startswith('rat'):
            while True:
                for channel in message.guild.voice_channels:
                    if len(channel.members) == 0:
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

                        # while len(channel.members) == 1:
                        #     time.sleep(1)

                        audio = discord.FFmpegPCMAudio(NOISE)
                        print('Playing' + NOISE)
                        voice.play(audio, after=None)

                        while voice.is_playing():
                            time.sleep(1) 

                        await voice.disconnect()
                        print('Spooked!')

                    else:
                        print(channel.name + ' is not empty')
                time.sleep(60)

client = MyClient()
client.run(TOKEN)
