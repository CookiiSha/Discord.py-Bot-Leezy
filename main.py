
import discord
import os, datetime, asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = '>>', intents = intents )

load_dotenv()

TOKEN = os.getenv("TOKEN")
@client.event 
async def on_ready():
    print("Leezy Bot is Running!")
    bot_is_online_channel = await client.fetch_channel('969906142832627712')
    show_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    await bot_is_online_channel.send(f"Leezy Bot is Running | {show_date}")


# Load, Unload, and Reload Functions 
@client.command(brief = "Loads an Extension")
@has_permissions(administrator = True)
async def load(ctx, extension):
    bot_is_online_channel = await client.fetch_channel('969906142832627712')
    
    try:
        # All cogs are named in lower case so everytime a user inputs a cog name it is automatically converted to Lower case
        await client.load_extension(f'cogs.{str(extension).lower()}')
        await bot_is_online_channel.send(f"Loaded '{extension}' Successfully")

        # Print Exception if the cog failed to load
        # Usually happens if the cog is already loaded or if the cog is unavailable
    except Exception as e :
        await bot_is_online_channel.send("Failed to Load Bot!")
        await bot_is_online_channel.send(f"```{e}```")
    
@client.command(brief = "Unloads an Extension")
@has_permissions(administrator = True)
async def unload(ctx, extension): 
    bot_is_online_channel = await client.fetch_channel('969906142832627712')
    
    try:
    # All cogs are named in lower case so everytime a user inputs a cog name it is automatically converted to Lower case
        await client.unload_extension(f'cogs.{str(extension).lower()}')
        await bot_is_online_channel.send(f"Unloaded '{extension}' Successfully")

    # Print Exception if the cog failed to load
    # Usually happens if the cog is already loaded or if the cog is unavailable
    except Exception as e :
        await bot_is_online_channel.send("Failed to Unload Bot!")
        await bot_is_online_channel.send(f"```{e}```")

@client.command(brief = "Reloads all extensions")
@has_permissions(administrator = True)
async def reload(ctx, extension = ''):
    bot_is_online_channel = await client.fetch_channel('969906142832627712')
    
    if extension == '': 
        loaded = []
        failed = []
        for filename in os.listdir('./cogs'):
            if(filename.endswith('.py')):
                try:
                    await client.unload_extension(f'cogs.{filename[:-3]}')
                    await client.load_extension(f'cogs.{filename[:-3]}')
                    loaded.append(filename[:-3])
                except Exception as e: 
                    failed.append(filename[:-3])
                    
        # Creates a message to send when the cogs are loaded 
        message = "```Loaded Cogs \n"
        for cogs in loaded: 
            message += f"- {cogs}\n"
        # Shows a List of Failed to Reload cogs if there are cogs that failed to load 
        if len(failed) > 0:
            message += "---------------------\nFailed to Load Cogs\n"
            for cogs in failed: 
                message += f"- {cogs}\n"
        message += "```"
        # Sends  the created message 
        await ctx.send(message)  
                    
    else:
        try:
        # All cogs are named in lower case so everytime a user inputs a cog name it is automatically converted to Lower case
            await client.unload_extension(f'cogs.{str(extension).lower()}')
            await client.load_extension(f'cogs.{str(extension).lower()}')
            await bot_is_online_channel.send(f"Reloaded '{extension}' Successfully")

        # Print Exception if the cog failed to load
        # Usually happens if the cog is already loaded or if the cog is unavailable
        except Exception as e :
            await bot_is_online_channel.send("Failed to Reload Bot!")
            await bot_is_online_channel.send(f"```{e}```")
        
# Error Handler 
@client.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the right permission to do this!")
    else: 
        await ctx.send(error)

# Loads Extensions on Start 

async def main(): 
    async with client: 
        await load_cogs()
        await client.start(TOKEN)

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if(filename.endswith('.py')):
            await client.load_extension(f'cogs.{filename[:-3]}')

    
asyncio.run(main())
