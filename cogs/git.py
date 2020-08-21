import discord
from discord.ext import commands
import pandas as pd
from utils.checks import owner_check


class LearnGit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(owner_check)
    async def gitAll(self, ctx):
        """Prints every git command available"""
        df = pd.read_csv(
            "https://raw.githubusercontent.com/LastAeon77/CSbot/master/Data/gitInfo.csv"
        )
        temp = df["Name"]
        final_Str = ""
        for com in temp:
            final_Str += com + "\n"
        embed = discord.Embed()
        embed.color = 15844367
        embed.set_author(name="All git commands currently")
        embed.description = final_Str
        await ctx.send(embed=embed)

    @commands.command()
    async def git(self, ctx, *, arx: str):
        """Searches CSV for """
        df = pd.read_csv(
            "https://raw.githubusercontent.com/LastAeon77/CSbot/master/Data/gitInfo.csv"
        )
        df["Name"] = df["Name"].str.lower()
        row = df.loc[df["Name"] == arx.lower()]
        if not row.empty:
            row = row.fillna(0)
            embed = discord.Embed()
            temp = row["Name"].values[0].capitalize()
            embed.set_author(name=temp)
            embed.description = row["Info"].values[0]
            if row["Image"].values[0] != 0:
                embed.set_image(url=row["Image"].values[0])
            if row["Source"].values[0] != 0:
                embed.set_footer(text="Source = " + row["Source"].values[0])
            await ctx.send(embed=embed)
        else:
            otherdf = df[df.Name.str[:1].str.lower() == arx[:1].lower()]
            otherdf = otherdf["Name"]
            final_str = ""
            for names in otherdf:
                final_str = final_str + "> " + names + "\n"
            embed = discord.Embed()
            embed.set_author(name=f"We Couldn't find :{arx}")
            embed.description = "Did you mean: \n" + final_str
            embed.color = 3066993
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(LearnGit(bot))
