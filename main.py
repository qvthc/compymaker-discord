import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

def add_link(link):
    with open("links.txt", "a") as file:
        file.write(link + "\n")

def remove_link(link):
    with open("links.txt", "r") as file:
        lines = file.readlines()
    
    with open("links.txt", "w") as file:
        for line in lines:
            if line.strip() != link:
                file.write(line)

def count_links():
    with open("links.txt", "r") as file:
        lines = file.readlines()
    return len(lines)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def add(ctx, link):
    add_link(link)
    await ctx.send(f"Added {link} to links.txt")

@bot.command()
async def remove(ctx, link):
    remove_link(link)
    await ctx.send(f"Removed {link} from links.txt")

@bot.command()
async def link_count(ctx):
    count = count_links()
    await ctx.send(f"Number of links in links.txt: {count}")

bot.run("YOUR_BOT_TOKEN")
