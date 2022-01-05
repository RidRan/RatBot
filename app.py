import discord
from discord.ext import commands
import os
import asyncio

from discord.gateway import VoiceKeepAliveHandler

TOKEN = os.environ['TOKEN']

NOISE = 'scream.mp3'

class MyClient(discord.Client):

    alive = True

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

                        audio = discord.FFmpegPCMAudio(NOISE)
                        print('Playing' + NOISE)
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
                await asyncio.sleep(600)

client = MyClient() 
client.run(TOKEN)
