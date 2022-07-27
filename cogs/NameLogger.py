import json
import discord
from discord.ext import commands

class NameLogger(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client


    @commands.command(name = "logchannel",
                    usage="<Selects the operanting channel>",
                    description = "Selects the channel which the bot will log the names")
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def logchannel(self, ctx:commands.Context, channel):
        await ctx.send(f"Log Channel selected as {channel}")
        channel = channel[2:-1]

        with open(r'json\nameLogChannel.json', "r") as f:
            channels = json.load(f)

        channels[str(ctx.guild.id)] = channel

        with open(r'json\nameLogChannel.json', "w") as f:
            json.dump(channels, f, indent= 4)

def setup(client):
    client.add_cog(NameLogger(client))