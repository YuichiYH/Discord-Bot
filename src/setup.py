import json
import os
import discord
from discord.ext import commands

# Setup for Prefix

def get_prefix(client, message):

    with open('json\prefixes.json', "r") as f:
        prefixes = json.load(f)

    try:
        prefix = prefixes[str(message.guild.id)]
    
    except:    
        prefixes[str(message.guild.id)] = "|"

        with open('json\prefixes.json', "w") as f:
            json.dump(prefixes, f, indent=4)

    return(prefix)

client = commands.Bot(command_prefix=get_prefix)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

# On Ready

@client.event
async def on_ready():
    print('connected as {0}'.format(client.user))