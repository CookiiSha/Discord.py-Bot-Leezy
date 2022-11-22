from urllib.request import urlopen
import discord, json
from discord.ext import commands, tasks

class ForYou(commands.Cog): 
    def __init__(self, client):
        self.client = client
        self.change_status.start()   

    @tasks.loop(hours=1)
    async def change_status(self):
        channel = self.client.get_channel(1036176120808230962)
        quote = json.loads(urlopen("http://api.quotable.io/random").read())
        embed = discord.Embed(description=f'`{quote["content"]}`\n- {quote["author"]}')
        embed.set_thumbnail(url="https://www.kindpng.com/picc/m/139-1396506_black-and-white-icons-quote-hd-png-download.png")
        
        await channel.send(embed = embed)
    
async def setup(client):
    await client.add_cog(ForYou(client))