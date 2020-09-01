# import discord
from discord.ext import commands
import json
import os

bot = commands.Bot(command_prefix=commands.when_mentioned_or("c!"))
with open("resources/settings.json", "r") as f:
    bot.config = json.load(f)


@bot.event
async def on_ready():
    """Tells owner that bot is ready"""
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


@bot.command()
async def test(ctx):
    """For testing if Bot is alive"""
    await ctx.channel.send("I'm alive! At least...")


@bot.command()
async def paidBy(ctx):
    """Joke"""
    await ctx.channel.send(
        "This is how the creator is getting paid: \nhttps://www.youtube.com/watch?v=DOfKWlAjJec"
    )


@bot.command()
async def backquote(ctx):
    """My computer can't type backward single quote"""
    await ctx.channel.send("`")


if __name__ == "__main__":  # check if in main
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            try:
                bot.load_extension("cogs." + os.path.splitext(file)[0])
                print(f"Extension {file} loaded.")
            except Exception as e:
                print(f"Failed to load extension {file}: {e}")

    bot.run(bot.config["discord"]["token"])
