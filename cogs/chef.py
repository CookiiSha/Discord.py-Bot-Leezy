from urllib.request import urlopen, Request
import discord, json
from discord.ext import commands
from discord.ui import Button, View
from .admin import Prefix
import re, os
from dotenv import load_dotenv
# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 

load_dotenv()
api_key = os.getenv("SPOONACULAR_API")

class Recipe(commands.Cog): 
    def __init__(self, client): 
        self.client = client

    @commands.command(name = "recipe")
    async def searchRecipe(self, ctx, mode,  *tags): 
        # json_url = urlopen(f"https://opentdb.com/api_category.php")
        # data = json.loads(json_url.read())
    
        if(mode == "random"): 

            description = ""

            site= f"https://api.spoonacular.com/recipes/random?apiKey={api_key}&number=1&tags={','.join(tags)}"
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(site,headers=hdr)
            json_url = urlopen(req)
            data = json.loads(json_url.read())


            for recipe in data["recipes"]:
                description+=f"**Summary**: \n{cleanhtml(recipe['summary'])}\n\n**Time to Make**: {recipe['readyInMinutes']} minutes\n\n**Good for** {recipe['servings']}\n\n**Price per serving**: ${'{:.2f}'.format(float(recipe['pricePerServing'] / 10))} *(Not Accurate)*"
                print(recipe["title"])
                embed = discord.Embed(title=recipe["title"], description=description, color=0xff2252)

                embed.set_author(name = "Spoonacular", icon_url="https://play-lh.googleusercontent.com/uOZlIZUJ7R79qs_J_a9cdxrJaGhHwqKTmika25Lp1vTeC1qe9lPQF5jalEFc8Htk7nQ")
                try:
                    embed.set_image(url=recipe["image"])
                except: 
                    embed.set_image(url="https://i0.wp.com/www.mimisrecipes.com/wp-content/uploads/2018/12/recipe-placeholder-featured.jpg")
                embed.set_footer(text = "id: " + str(recipe["id"])) 
                

                link_button = Button(label="Link to Source", url = recipe["sourceUrl"])

                cancel_button = Button(label="Pass", style = discord.ButtonStyle.danger )

                async def cancel_callback(interaction):
                    embed = discord.Embed(title = "You closed this Recipe.")
                    embed.set_author(name = "Spoonacular", icon_url= "https://play-lh.googleusercontent.com/uOZlIZUJ7R79qs_J_a9cdxrJaGhHwqKTmika25Lp1vTeC1qe9lPQF5jalEFc8Htk7nQ") 
                    await interaction.response.edit_message(embed = embed)
                    
                cancel_button.callback = cancel_callback

                view = View()
                view.add_item(link_button)
                view.add_item(cancel_button)

                await ctx.send(embed = embed, view = view)
                



def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext
        
async def setup(client):
    await client.add_cog(Recipe(client))