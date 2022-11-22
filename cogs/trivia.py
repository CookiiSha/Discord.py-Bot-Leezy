
from urllib.request import urlopen
import discord, json, random, os
from discord.ext import commands

from .admin import Prefix
from .economy import add_to_wallet
import base64

class Trivia(commands.Cog): 
    def __init__(self, client): 
        self.client = client
    
    @commands.command(name = "trivia", brief = "Starts a Trivia Game", description = "Starts a Trivia Game\nIf you type `=trivia` with no arguments, gives a random question category and difficulty\nExample: =trivia 1 easy\nThis will give you a quiz with a category of General Knowledge and difficulty of `Easy`\n\nType =trivia category for a list of all category ids", usage = "[category] [difficulty]" )
    async def trivia(self, ctx,  category: str = None, difficulty = None,):
        
        # ----------------- PRINTING THE CATEGORY LIST --------------------
        if(category != None and category.lower() == "category"):
            json_url = urlopen(f"https://opentdb.com/api_category.php")
            data = json.loads(json_url.read())

            description = ""
            # Number variable is for the numbering of the categories
            number = 1
            for category in data["trivia_categories"]:
                description += str(number) + ".) " + category["name"] + "\n"
                number += 1

            embed=discord.Embed(title="List of Categories", description = description, color=0xfff22e)
            await ctx.send(embed = embed)
        # ---------------- PRINTING THE CATEGORY LIST -----------------------
        else:
            api_url = "https://opentdb.com/api.php?amount=1&type=multiple&encode=base64"
            if(category != None): 
                try:
                    if(int(category) >= 1 and int(category) <= 24):
                        api_url += f"&category=" + str(int(category) + 8)
                    else: 
                        await ctx.send(f"Please enter a number between 1 - 24. See list of category here `{Prefix}trivia category`")
                        return
                except:
                    await ctx.send("Incorrect usage for Trivia Command `=trivia [category] [difficulty]`. type `=trivia category` for a list of categories.")
                    return

            if(difficulty != None and difficulty.lower() in ["easy", "medium", "hard"]): 
                api_url += "&difficulty=" + difficulty.lower()

            else: 
                api_url = f"https://opentdb.com/api.php?amount=1&type=multiple&encode=base64"

            json_url = urlopen(api_url)
            data = json.loads(json_url.read())

            # ---------------------------- VARIABLES ---------------------------------
            question = ""
            choices = []
            answer = ""
            difficulty = ""
            category = ""
            one_emoji = "<:one_:1008272802257846352>"
            two_emoji = "<:two_:1008272824768667679>"
            three_emoji = "<:three_:1008272830183518308>"
            four_emoji = "<:four_:1008272828031836271>"
            reward = 0
            cost = 0
            # ---------------------------- VARIABLES ------------------------------------

            # Setting up the Trivia Question
            for trivia_question in data["results"]:
                answer = convertBase64(trivia_question["correct_answer"])
                for choice in trivia_question["incorrect_answers"]:
                    choices.append(convertBase64(choice))
                choices.append(answer)
                difficulty = convertBase64(trivia_question["difficulty"])
                category = convertBase64(trivia_question["category"])
                random.shuffle(choices)
                question = convertBase64(trivia_question["question"])

            if(difficulty == "easy"): 
                reward = random.randint(30, 50)
                cost = -random.randint(1, 10)
            elif(difficulty == "medium"):
                reward = random.randint(60, 90)
                cost = -random.randint(10, 20)
            elif(difficulty == "hard"):
                reward = random.randint(100, 200)
                cost = -random.randint(20, 30)

            # Creating Embed 
            embed=discord.Embed(title="Leezy Trivia", url="", description=f"**{question}** \nYou have 30 seconds to answer\n\n:one:  {choices[0]}\n\n:two:  {choices[1]}\n\n:three:  {choices[2]}\n\n:four:  {choices[3]}\n", color=0xf54747)
            embed.add_field(name="Difficulty", value=difficulty, inline=True)
            embed.add_field(name="Category", value=category, inline=True)
            # Setting up the questions and choices
            quiz = await ctx.send(embed=embed)
            await quiz.add_reaction(one_emoji)
            await quiz.add_reaction(two_emoji)
            await quiz.add_reaction(three_emoji)
            await quiz.add_reaction(four_emoji)
            
            # -------------------------- WAITING FOR USER INPUT ------------------------------------------
            def check(reaction, user): 
                return user == ctx.author and str(reaction.emoji) in (one_emoji, two_emoji, three_emoji, four_emoji)
            
            user_answer = ""
            try: 
                reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
            except: 
                embed=discord.Embed(title=f"You Ran Out Of Time!", description = f"**{question}**\nThe answer to that is **{answer}**\n\n**You Lost {cost} IQ points**", color=0xf54747)
                await quiz.clear_reactions()
                await quiz.edit(embed = embed)
                await add_to_wallet(ctx.author, cost)


            if str(reaction.emoji) == one_emoji:
                user_answer = choices[0]
            elif str(reaction.emoji) == two_emoji:
                user_answer = choices[1]
            elif str(reaction.emoji) == three_emoji:
                user_answer = choices[2]
            elif str(reaction.emoji) == four_emoji:
                user_answer = choices[3]
            else: 
                pass
            # ------------------------------ WAITING FOR USER INPUT ------------------------------------

            # Check if the Answer is correct Or Not 
            if(user_answer == answer): 
                embed=discord.Embed(title=f"CORRECT ANSWER!", description = f"**{question}**\nYou answered **{answer}**", color=0x2eff37)
                embed.add_field(name = "Reward Given", value = str(reward))
                await quiz.clear_reactions()
                await quiz.edit(embed = embed)

                # Giving money to user if the Answer is correct
                await add_to_wallet(ctx.author, reward)    

            else: 
                embed=discord.Embed(title=f"Incorrect!", description = f"**{question}**\n You answered **{user_answer}** \nBut the answer was **{answer}**\n\n**You Lost {cost} IQ points**", color=0xf54747)
                await quiz.clear_reactions()
                await quiz.edit(embed = embed)
                await add_to_wallet(ctx.author, cost)

    # # NOT YET FINISH
    # @commands.command(name = "multrivia")
    # async def multrivia(self, ctx):
    #     all_questions = []
    #     api_url = ""

    #     json_url = urlopen(api_url)
    #     data = json.loads(json_url.read())
    #     for question in data["results"]: 
    #         print(question)
    #         all_questions.append(Question(
    #             question["category"],
    #             question["type"], 
    #             question["difficulty"], 
    #             question["question"],
    #             question["correct_answer"], 
    #             question["incorrect_answers"]
    #         ))
    #     await ctx.send(f"```{all_questions.pop().get_question()}```")
    #     embed=discord.Embed(title="Leezy Trivia", url="https://opentdb.com/api_config.php", description="**What is my name** \nasdasd", color=0xf54747)
    #     embed.set_author(name="Leezy Trivia Quiz", url="https://opentdb.com/api_config.php", icon_url="https://opentdb.com/api_config.php")
    #     embed.add_field(name="Difficulty", value="Diff", inline=True)
    #     embed.add_field(name="Category", value="Mathematics ", inline=True)
    #     embed.add_field(name="Coins ", value="46", inline=True)
    #     await ctx.send(embed=embed)

# convers base64 values
def convertBase64(code):
        converted = base64.b64decode(code).decode("utf-8", "ignore")
        return converted

async def setup(client):
    await client.add_cog(Trivia(client))