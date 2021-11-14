import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True

TOKEN = os.environ['TOKEN']

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    if bot.user != message.user:
         await bot.send_message(message.channel, 'Eeek!')

bot.run(TOKEN)
