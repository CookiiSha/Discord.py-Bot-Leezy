import discord, json
from urllib.request import urlopen
from discord.ext import commands

class Cat(commands.Cog):
    def __init__(self, client): 
        self.client = client

    @commands.command(name="cat")
    async def catFact(self, ctx, mode):
        url = "https://catfact.ninja/fact?max_length=140"
        json_url = urlopen(url)
        data = json.loads(json_url.read())
        if(mode == "fact"):
            image = json.loads(urlopen("https://api.thecatapi.com/v1/images/search").read())
            embed = discord.Embed(description=f'**DID YOU KNOW?**\n{data["fact"]}', color=0x66246f)
            for i in image: 
                embed.set_thumbnail(url=i["url"])
            embed.set_author(name = "Cat Facts", icon_url="https://cdn-icons-png.flaticon.com/512/616/616430.png")
            await ctx.send(embed = embed)
    
async def setup(client): 
    await client.add_cog(Cat(client))