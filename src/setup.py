import json
from logging import exception
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

# Manual Functions

# Finds the guild by the name
def find_guild_id(name):
    print(name)

    for guild in client.guilds:

        print(guild.name.lower().replace(" ", ""))
        if guild.name.lower().replace(" ", "") == name.lower():
            return guild.id

# Show all servers
def servers(*args):
    """Show all servers that the bot is logged"""

    for guild in client.guilds:
        print(" - " + guild.name)

# Show all chats
def chat(*guild):
    """Show all chats inside that server

    Parameters
    ----------

    guild: str
        The name of the server
    """

    server = client.get_guild(find_guild_id("".join(guild)))

    for chat in server.channels:
        print(" - " + chat.name)
        print("  > " + str(chat.id))

async def message(chat_id, *message):
    """Sends a message in the chat
    
    Parameters
    ----------
    chat_id: 
        id of the chat you want to send the message

    message:
        The content of the message you want to send
    """

    try:
        channel = client.get_channel(int(chat_id))
    except Exception as e:
        print(e)
    await channel.send("".join(message))

command = ["","",""]

case = {
    "servers" : servers,
    "guilds" : servers,
    "chats" : chat,
    "channels" : chat,
    "send" : message,
    "message" : message
}


# Ping test

@client.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Check if files exist

if not(exists("./json")):
    os.mkdir('./json')

# On Ready

@client.event
async def on_ready():
    print('connected as {0}'.format(client.user))

    #runs a loop for the commands
    while True:
        command = str.split(input("Command \n"), " ")

        command.append("")
        command.append("")

        try:
            await case[command[0]](command[1], command[2])

        except Exception as e:
            print(e)
