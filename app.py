import discord
from discord.ext import commands
import os
import time

from discord.gateway import VoiceKeepAliveHandler

TOKEN = os.environ['TOKEN']

NOISE = 'scream.mp3'

class MyClient(discord.Client):
    init = False

    serverSet = set()
    serverIndex = 0
    channelIndex = 0

    async def on_ready(self):
        print('Logged in as ' + self.user.name + ' (' + str(self.user.id) + ')')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.content.startswith('rat_test'):
            voices = self.voice_clients
            voice = None
            for v in voices:
                if v.guild.id == message.guild.id:
                    voice = v
            print(voice)
            for s in self.serverSet:
                print(s.name)
        if message.content.startswith('rat_add'):
            self.serverSet.add(message.guild)
            # reply = 'Name: ' + message.author.name
            # await message.channel.send(reply)
        if message.content.startswith('rat_init'):
            if self.init == False:
                while True:
                    for s in self.serverSet:
                        for vc in s.voice_channels:
                            if len(vc.members) == 0:
                                voices = self.voice_clients
                                voice = None
                                for v in voices:
                                    if v.guild.id == message.guild.id:
                                        voice = v

                                if voice and voice.is_connected():
                                    await voice.move_to(vc)
                                else:
                                    voice = await vc.connect()

                                print('Joined ' + vc.name + " (" + len(vc.members) + " members) in " + s.name)

                                self.init = True

                                while len(vc.members) == 0:
                                    time.sleep(1)

                                audio = discord.FFmpegPCMAudio(NOISE)
                                print('Playing' + NOISE)
                                voice.play(audio, after=None)
                                while voice.is_playing():
                                    time.sleep(1) 

                                await voice.disconnect()
                            else:
                                print(vc.name + " is not empty")
                    print("Looping back")
            else:
                await message.channel.send('The Rat is already awake')

client = MyClient()
client.run(TOKEN)
