import discord
from discord.ext import commands

class SFW(commands.Cog): 
    def __init__(self, client): 
        self.client = client

    @commands.command(name = "wave")
    async def wave(self, ctx, *message):
        print("S")

async def setup(client):
    await client.add_cog(SFW(client))