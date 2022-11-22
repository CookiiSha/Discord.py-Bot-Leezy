from pydoc import describe
from urllib.parse import uses_fragment
import discord, json
from discord.ext import commands

class Economy(commands.Cog): 
    def __init__(self, client): 
        self.client = client

    @commands.command(name = "balance", description = "Shows your Wallet and Bank Account", brief = "Shows Balance", usage = "[user]")
    async def balance(self,ctx): 
        await open_account(ctx.author)

        users = await get_bank_data()

        wallet = users[str(ctx.author.id)]["wallet"]
        bank = users[str(ctx.author.id)]["bank"]
        embed = discord.Embed(title = f"{ctx.author.name}'s balance", color=0xf54747)

        if(int(wallet)) < 0: 
            embed.set_author(name = "YOU'RE BROKE PLEASE ANSWER MORE TRIVIA QUESTIONS")
        embed.add_field(name = "Wallet balance", value = wallet)
        embed.add_field(name = "Bank balance", value = bank)
        embed.add_field(name = "------------------------------------------", value = "------------------------------------------", inline = False)
        embed.set_footer(text = "Most features in economy doesn't work. This Economy is only used for the leaderboards as of now. Sorry... q.q", icon_url="https://emoji.discord.st/emojis/8e585313-937f-40bd-97e8-302b12ca360a.png")
        await ctx.send(embed = embed)

    @commands.command(name="leaderboard", description = "Who is the richest", brief = "Shows Leaderboard")
    async def leaderboard(self, ctx, amount = 3): 
        users = await get_bank_data()
        leaderboard = {}
        total = []
        for user in users: 
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leaderboard[total_amount] = name
            total.append(total_amount)
        
        total = sorted(total, reverse=True)
        embed = discord.Embed(title = f"Top {amount} Smartest People", color = 0x34ff5f)
        index = 1
        for num in total: 
            id_ = leaderboard[num]
            member =await self.client.fetch_user(id_)
            try: 
                name = member.name
            except: 
                name = "Anonymous"
            embed.add_field(name = f"{index}. {name}", value = f"IQ Points: {num}", inline = False)
            if index == amount: 
                break
            else: 
                index += 1
        
        await ctx.send(embed = embed)

async def open_account(user): 
    users = await get_bank_data()

    if str(user.id) in users: 
        return False
    else: 
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 50
        users[str(user.id)]["bank"] = 0
    
    with open("./jsons/mainbank.json", "w") as f:
        json.dump(users, f)

async def get_bank_data(): 
    with open("./jsons/mainbank.json", "r") as f: 
        users = json.load(f)

    return users

async def add_to_wallet(user, amount): 
    await open_account(user)
    users = await get_bank_data()
    users[str(user.id)]["wallet"] += amount
    with open("./jsons/mainbank.json", "w") as f: 
        json.dump(users, f)


async def setup(client):
    await client.add_cog(Economy(client))