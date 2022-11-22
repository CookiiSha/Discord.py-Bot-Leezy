from discord.ui import Button, View
import discord, os, random
from discord.ext import commands
from pexels_api import API
from dotenv import load_dotenv
# ----------------- VARIABLES ---------------------
load_dotenv()
pexels = API(os.getenv("PEXELS_API"))


class Search(commands.Cog): 
    def __init__(self, client): 
        self.client = client

    @commands.command(name = "picture")
    async def search(self, ctx, *,search): 
        pexels.search("".join(search), page=1, results_per_page=100)
        # Get photo entries
        photos = pexels.get_entries()
        selected_photos = []
        # Loop the five photos
        print(photos)
        for photo in photos:
        # Print photographer
            selected_photos.append(photo)
            print(photo.description)
        
        photo = selected_photos[random.randint(0, len(selected_photos) - 1)]
        try:
                embed = discord.Embed()
                embed.set_image(url=photo.original)
                embed.set_author(name = "Pexels", icon_url= "https://theme.zdassets.com/theme_assets/9028340/1e73e5cb95b89f1dce8b59c5236ca1fc28c7113b.png") 

                link_button = Button(label="Download Image", url = photo.url)

                cancel_button = Button(label="Pass", style = discord.ButtonStyle.danger )

                async def cancel_callback(interaction):
                    embed = discord.Embed(title = "You passed this Image.")
                    embed.set_author(name = "Pexels", icon_url= "https://theme.zdassets.com/theme_assets/9028340/1e73e5cb95b89f1dce8b59c5236ca1fc28c7113b.png") 
                    await interaction.followup.edit(embed = embed)
                    
                cancel_button.callback = cancel_callback

                view = View()
                view.add_item(link_button)
                view.add_item(cancel_button)

                await ctx.send(embed = embed, view=view)

        except Exception as e: 
            print(e)

        
async def setup(client):
    await client.add_cog(Search(client))