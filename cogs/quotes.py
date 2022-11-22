from email.quoprimime import quote
import discord, json
from discord.ext import commands
from urllib.request import urlopen
class Quotes(commands.Cog): 
    def __init__(self, client): 
        self.client = client

    @commands.command(name="quote")
    async def quote(self, ctx, *tags): 
        if tags[0] == "tags": 
            data = json.loads(urlopen("http://api.quotable.io/tags").read())
            description = ""
            i = 1 
            for tag in data: 
                description += f'{i}.) `{tag["name"]}`\n'
                i+=1 
            embed = discord.Embed(title = "List of Quote Tags", description=description)    
            await ctx.send(embed = embed)

        else:
            if tags == None: 
                quote = json.loads(urlopen("http://api.quotable.io/random").read())
            if tags[0] == "popular":
                quote = json.loads(urlopen(f"http://api.quotable.io/random/?tags=famous-quotes").read())
            else: 
                quote = json.loads(urlopen(f"http://api.quotable.io/random/?tags={','.join(tags)}").read())
            embed = discord.Embed(description=f'`{quote["content"]}`\n- {quote["author"]}')
            await ctx.send(embed = embed)


async def setup(client): 
    await client.add_cog(Quotes(client))
