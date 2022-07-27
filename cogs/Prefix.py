import json
import discord
from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client


    @commands.command(name = "commandName",
                    usage="<usage>",
                    description = "description")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context):
        await ctx.send("template command")

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

    @commands.command()
    async def changeprefix(ctx, prefix):
        with open('json\prefixes.json', "r") as f:
            prefixes = json.load(f)
        
        prefixes[str(ctx.guild.id)] = prefix

        with open('json\prefixes.json', "w") as f:
            json.dump(prefixes, f, indent=4)        
    

def setup(client):
    client.add_cog(Prefix(client))