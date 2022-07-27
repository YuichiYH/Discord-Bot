import json
import discord
from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(guild):
        with open('json\prefixes.json', "r") as f:
            prefixes = json.load(f)
        
        prefixes[str(guild.id)] = "|"

        with open('json\prefixes.json', "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(guild):
        with open('json\prefixes.json', "r") as f:
            prefixes = json.load(f)
        
        prefixes.pop(str(guild.id))

        with open('json\prefixes.json', "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.command(name= "changeprefix", usage = "Changes the bot prefix", description = "Changes the bot prefix")
    async def changeprefix(self, ctx, prefix):
        with open('json\prefixes.json', "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open('json\prefixes.json', "w") as f:
            json.dump(prefixes, f, indent=4)      

        await ctx.send(f"Prefix changed to {prefix}")  
    

def setup(client):
    client.add_cog(Prefix(client))