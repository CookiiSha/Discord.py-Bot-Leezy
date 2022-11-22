import discord, random,json
from discord.ext import commands
from urllib.request import urlopen
from discord.ui import Button, View
class Hmtaii(commands.Cog): 
    def __init__(self, client): 
        self.client = client

    @commands.command(name = "nsfw")
    @commands.is_nsfw()
    async def nsfw(self, ctx, category = None):
        categories = ["anal", "ass","bdsm", "cum", "classic", "creampie", "manga", "femdom", "hentai", "incest", "masturbation", "public", "ero", "orgy", "elves", "yuri", "pantsu", "glasses", "cuckold", "blowjob", "boobjob", "footjob", "handjob", "boobs", "thighs","pussy","ahegao", "uniform", "gangbang","tentacles","gif","nsfwNeko", "nsfwMobileWallpaper","zettaiRyouiki"]
        link = f"https://hmtai.herokuapp.com/v2/"
        if(category == "list"):
            description = ""
            i = 1
            for c in categories: 
                description+=f"{i}.) `{c}`\n"
                i+=1

            embed = discord.Embed(title = f"List of Categories", description=description, color=0x23f8ff)
            embed.set_author(name = "Leezy Bot")
            await ctx.send(embed=embed)
            return
        elif(category in categories):
            link += f"{category}"

        else: 

            link += categories(random.randint(0, len(categories) - 1))
        json_url = urlopen(link)
        data = json.loads(json_url.read())

        embed = discord.Embed(title = f"You searched for `{category}`", color=0x23f8ff)
        embed.set_author(name = "Leezy Bot")
        embed.set_image(url=data["url"])


        link_button = Button(label="Download", url=data["url"], emoji="😈")
        cancel_button = Button(label="Pass", style = discord.ButtonStyle.danger )

        async def cancel_callback(interaction):
            embed = discord.Embed(title = "Removed Image", color=0x23f8ff)
            embed.set_author(name = "Leezy Bot")
            await interaction.response.edit_message(embed = embed)

        cancel_button.callback = cancel_callback

        view = View()
        view.add_item(link_button)
        view.add_item(cancel_button)
        await ctx.send(embed=embed, view=view)


       

    @commands.command(name = "sfw")
    async def sfw(self, ctx, category): 
        categories = [
            "wave", 
            "wink",
            "tea",
            "bonk", 
            "punch", 
            "poke", 
            
        ]
        link = f"https://hmtai.herokuapp.com/v2/"
        if(category in categories):
            link += f"{category}"
        else: 
            link += categories(random.randint(0, len(categories) - 1))
        embed = discord.Embed(name = f"You searched for `{category}`")
        embed.set_author("Leezy Bot")
        embed.set_image(url=link)
        await ctx.send(embed=embed)
async def setup(client):
    await client.add_cog(Hmtaii(client))