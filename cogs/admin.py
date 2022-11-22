
import discord,os
from discord.ext import commands
from discord.ext.commands import has_permissions
from dotenv import load_dotenv

load_dotenv()
Prefix = os.getenv("PREFIX")
class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name = "ping", description = "Returns a pong", usage = "[optional: mention]", brief = "Replies Pong")
    async def ping(self, ctx: commands.Context, user: discord.Member = None):
        # Pings the mentioned user 
        try:
            await ctx.send(f"Hi! {user.mention}, {ctx.author} is mentioning you!")
        # Sends a pong
        except: 
            await ctx.send(f"pong")
    
    # Clear Command, Removes an amount of messages depending on the argument given. 
    # Checks if the bot has permission to manage messages
    @commands.command(name = "clear", description = "Clears a number of messages in the channel. if no argument is given, purges 5 messages.", usage = f"[amount]", brief = "Clears Messages")
    @has_permissions(manage_messages = True)
    async def clear(self, ctx, amount:int = None):
        # Checks if there is an argument or not
        if amount == None:
            await ctx.channel.purge(limit = 5)
        else: 
            await ctx.channel.purge(limit = amount)

async def setup(client):
    await client.add_cog(Admin(client))
