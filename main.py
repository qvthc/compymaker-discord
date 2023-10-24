import discord, json
from discord.ext import commands

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    TOKEN = config["token"]
    PREFIX = config["prefix"]

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

def is_link_duplicate(link):
    with open("links.txt", "r") as file:
        return link in file.read()

async def send_embed(ctx, title, description, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)


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
    if is_link_duplicate(link):
        await send_embed(ctx, "Duplicate Link", f"{link} is already in links.txt.", discord.Color.red())
    else:
        add_link(link)
        await send_embed(ctx, "Link Added", f"Added {link} to links.txt.", discord.Color.green())

@bot.command()
async def remove(ctx, link):
    if is_link_duplicate(link):
        remove_link(link)
        await send_embed(ctx, "Link Removed", f"Removed {link} from links.txt.", discord.Color.green())
    else:
        await send_embed(ctx, "Link Not Found", f"{link} not found in links.txt.", discord.Color.red())

@bot.command()
async def link_count(ctx):
    count = count_links()
    await send_embed(ctx, "Link Count", f"Number of links in links.txt: {count}", discord.Color.blue())

@bot.command()
async def purge(ctx, num: int):
    try:
        await ctx.channel.purge(limit=num)
        await send_embed(ctx, "Purge Complete", "Messages have been removed.", discord.Color.green())
    except Exception as e:
        await send_embed(ctx, "Purge Failed", f"An error occurred: {e}", discord.Color.red())

@bot.command()
async def get_links(ctx):
    await ctx.send(file=discord.File("links.txt"))
    
bot.run(TOKEN)
