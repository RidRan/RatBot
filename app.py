import discord
from discord.ext import commands
import os
import asyncio
import random

from discord.gateway import VoiceKeepAliveHandler

TOKEN = os.environ['TOKEN']

NOISE = 'noise'
FILEEXT = '.mp3'

class MyClient(discord.Client):

    alive = True

    sleep = 600

    async def on_ready(self):
        print('Logged in as ' + self.user.name + ' (' + str(self.user.id) + ')')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return
        if message.content.startswith('kill rat'):
            self.alive = False
            voices = self.voice_clients
            voice = None
            for v in voices:
                if v.guild.id == message.guild.id:
                    voice = v

            if voice and voice.is_connected():
                await voice.disconnect()
        if message.content.startswith('sleepy'):
            delay = int(message.content.split(' ')[1])
            self.sleep = delay
            print('Sleep delay set to ' + str(self.sleep) + ' seconds')
        if message.content.startswith('daddy'):
            await message.channel.send('Cameron Collingham')
        if message.content.startswith('rat'):
            self.alive = True
            while self.alive:
                for channel in message.guild.voice_channels:
                    if len(channel.members) == 0 and len(channel.changed_roles) == 0:

                        voices = self.voice_clients
                        voice = None
                        for v in voices:
                            if v.guild.id == message.guild.id:
                                voice = v

                        print('Joining ' + channel.name)
                        if voice and voice.is_connected():
                            await voice.move_to(channel)
                        else:
                            voice = await channel.connect()

                        print('Joined ' + channel.name + ' (' + str(len(channel.members)) + ' members) in ' + channel.guild.name)

                        while len(channel.members) <= 1:
                            await asyncio.sleep(1)

                        chance = random.random()
                        choice = 1
                        if chance < .05:
                            choice = 5
                        elif chance < .15:
                            choice = 4
                        elif chance < .3:
                            choice = 1
                        elif chance < .55:
                            choice = 3
                        else:
                            choice = 2

                        audio = discord.FFmpegPCMAudio(NOISE + str(choice) + FILEEXT)
                        print('Playing' + NOISE + str(choice) + FILEEXT)
                        voice.play(audio, after=None)

                        while voice.is_playing():
                            await asyncio.sleep(1) 

                        await voice.disconnect()
                        
                        for m in voice.channel.members:
                            if m.name != 'RatBot':
                                await message.channel.send('Spooked by ' + m.name)
                                print('Spooked by ' + m.name)
                                break
                        
                    else:
                        print(channel.name + ' is not empty')
                print('Sleeping')
                await asyncio.sleep(self.sleep)

client = MyClient() 
client.run(TOKEN)
