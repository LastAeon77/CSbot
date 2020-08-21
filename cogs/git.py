import discord
from discord.ext import commands
import pandas as pd


class CSsearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def git(self, ctx, *, arx: str):
        """Searches CSV for """
        df = pd.read_csv(
            "https://raw.githubusercontent.com/LastAeon77/CSbot/master/Data/searchCpp.csv"
        )
        df["Name"] = df["Name"].str.lower()
        row = df.loc[df["Name"] == arx.lower()]
        if not row.empty:
            embed = discord.Embed()
            embed.set_author(name=row["Name"][0].capitalize())
            embed.description = row["Info"]
            if not row["Image"][0].empty:
                embed.set_image(url=row["Image"][0])
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
    bot.add_cog(CSsearch(bot))
