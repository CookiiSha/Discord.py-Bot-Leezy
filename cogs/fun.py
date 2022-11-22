import asyncio
from dis import disco
import discord
from discord.ext import commands
import random 

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="ask", description="Ask Questions and find Answers", usage = "[question]", brief = "Answers your questions")
    async def book_of_answers(self, ctx, *question):
        answers = []

        with open('./extras/book_of_answers.txt', 'r') as f:
            for line in f.read().splitlines():
                answers.append(line)

        if not question: 
            await ctx.send("**You didn't enter a question!**")
        else: 
            # Remove the original message and creates a searching for answer message and edits the original message and shows the answer    
            await ctx.channel.purge(limit=1)
            embed = discord.Embed(description="Searching For Answers", color=0x43ff29)
            embed.set_image(url="https://c.tenor.com/_w9iT5Eg5NQAAAAC/flip-book.gif")
            embed.set_author(name = "Book of Answers", icon_url="https://images-na.ssl-images-amazon.com/images/I/41ON8hhFmxL._SX383_BO1,204,203,200_.jpg")
            reply = await ctx.send(embed = embed)
            rng = random.randint(0, len(answers)-1)

            embed = discord.Embed( description=f"You asked `{' '.join(question[:])}`\n```{answers[rng]}```", color=0x2453ff)
            embed.set_author(name = "Book of Answers", icon_url="https://images-na.ssl-images-amazon.com/images/I/41ON8hhFmxL._SX383_BO1,204,203,200_.jpg")
            embed.set_thumbnail(url="https://thebookofanswers.com/wp-content/uploads/2018/10/boa_slider.png")

            await asyncio.sleep(3)
            await reply.edit(embed = embed)

    @commands.command(name="pp", description="Shows your pp size", brief = "Shows pp size")
    async def pp_size(self, ctx):
        cock = "8"
        cock_size = random.randint(0, 50)
        cock_sizes = cock_size
        while(cock_sizes > 0):
            cock_sizes-=1
            cock += "="
        cock+="D"
        if cock_size > 10:
            embed = discord.Embed(title="Omg that's HUGE!",
                    description=cock,
                    color=discord.Color.dark_grey())
        elif cock_size > 6:
            embed = discord.Embed(title="Above Average!",
                    description=cock,
                    color=discord.Color.dark_grey())
        elif cock_size > 4:
            embed = discord.Embed(title="Big Enough",
                    description=cock,
                    color=discord.Color.dark_grey())
        elif cock_size > 2:
            embed = discord.Embed(title="wow..",
                    description=cock,
                    color=discord.Color.dark_grey())
        else:
            embed = discord.Embed(title="..",
                    description=cock,
                    color=discord.Color.dark_grey())

        await ctx.send(embed = embed)

async def setup(client):
    await client.add_cog(Fun(client))