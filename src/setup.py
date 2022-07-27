import json
import os
import discord
from os.path import exists
from discord.ext import commands

# Intents

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

# Setup for Prefix

def get_prefix(client, message):

    with open('json\prefixes.json', "r") as f:
        prefixes = json.load(f)

    try:
        prefix = prefixes[str(message.guild.id)]
    
    except:    
        prefix = "|"
        prefixes[str(message.guild.id)] = "|"

        with open('json\prefixes.json', "w") as f:
            json.dump(prefixes, f, indent=4)
        

    return(prefix)

client = commands.Bot(command_prefix=get_prefix, intents=intents)

# Loads Cogs

for filename in os.listdir(".\src\cogs"):
    if filename.endswith(".py"):
        print(f'loaded cogs.{filename[:-3]}')
        client.load_extension(f'src.cogs.{filename[:-3]}')

# Ping test

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Check if files exist

if not exists("./json"):
    os.mkdir('./json')

# On Ready

@client.event
async def on_ready():
    print('connected as {0}'.format(client.user))