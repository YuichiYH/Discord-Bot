import json
import discord
from os.path import exists
from xml.etree.ElementTree import Comment
from discord.ext import commands


class NameLogger(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        if not(exists(r'json\nameLogChannel.json')):
            with open(r'json\nameLogChannel.json', 'x') as f:
                json.dump({}, f)

        if not(exists(r'json\nicks.json')):
            with open(r'json\nicks.json', 'x') as f:
                guilds = {}

                for guild in self.client.guilds:
                    guilds[str(guild.id)] = {}

                    nicks = guilds[str(guild.id)]

                    for member in guild.members:
                        nicks[str(member.id)] = member.nick
            
            json.dump(guilds, f, indent= 4)

        with open(r'json\nameLogChannel.json', 'r') as f:
            channels = json.load(f)

        with open(r'json\nicks.json', "r") as f:
            guilds = json.load(f)

        for guild in self.client.guilds:

            if not(str(guild.id) in guilds):
                guilds[str(guild.id)] = {}

            nicks = guilds[str(guild.id)]

            channel = self.client.get_channel(channels[str(guild.id)])
            
            for member in guild.members:

                currentNick = guild.get_member(member.id).display_name

                if not(str(member.id) in nicks):
                    nicks[str(member.id)] = currentNick

                oldNick = nicks[str(member.id)]

                if oldNick != currentNick:
                    await channel.send(f"<@{member.id}> changed its name from **{oldNick}** to **{currentNick}**")
                    nicks[str(member.id)] = currentNick

        with open(r'json\nicks.json', 'w') as f:
            json.dump(guilds, f, indent= 4)


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

        channels[str(ctx.guild.id)] = int(channel)

        with open(r'json\nameLogChannel.json', "w") as f:
            json.dump(channels, f, indent= 4)

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        if before.nick != after.nick:

            with open(r'json\nameLogChannel.json', "r") as f:
                channels = json.load(f)

            channelid = channels[str(after.guild.id)]

            channel = self.client.get_channel(channelid)

            await channel.send(f"<@{after.id}> changed its name from **{before.nick}** to **{after.nick}**")

def setup(client):
    client.add_cog(NameLogger(client))