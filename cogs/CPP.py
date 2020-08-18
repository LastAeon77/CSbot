import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import requests
import sys
import pandas as pd

pd.options.mode.chained_assignment = None
sys.path.insert(1, "./Api/")
from GoogleApi import google_query
from GoogleApi import api_key
from GoogleApi import cse_id


class Cpp:
    def __init__(self, searchTerm):
        k = google_query(searchTerm, api_key, cse_id, num=1)
        self.link = k[0]["link"]
        source = requests.get(self.link).text
        self.soup = BeautifulSoup(source, "lxml")

    def scrapeDescription(self):
        D = self.soup.find("section")
        # backward = BeautifulSoup("```", "lxml")
        description = D.get_text()[:500] + "..."
        return description

    def scrapeTable(self):
        df_list = pd.read_html(self.link)
        df = df_list[0]
        if len(df.index) > 1:
            df = df.iloc[:, :2]
            temp = df.definition.apply(
                lambda x: x.rsplit(maxsplit=len(x.split()) - 3)[0]
            )
            df.loc[:, ("definition")] = temp
            finalStr = ("```") + df.to_string(index=False) + ("```")
            return finalStr
        else:
            T = self.soup.find("table")
            table = ("```") + T.get_text() + ("```")
            return table

    def scrapeImg(self):
        Img = self.soup.find("img")
        image = self.link + Img["src"]
        return image

    def getTitle(self):
        k = self.link.split("/")
        title = k[-2]
        return title


class CSsearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cpp(self, ctx, *, arx: str):
        """Searches cplusplus for information"""
        loading = await ctx.send("Please wait a moment")
        topic = Cpp(arx)
        try:
            embed = discord.Embed()
            imageLink = ""
            try:
                imageLink = topic.scrapeImg()
                embed.set_image(url=imageLink)
            except:
                pass
            table = topic.scrapeTable()
            descript = topic.scrapeDescription()
            embed.set_author(name=topic.getTitle().capitalize())
            embed.description = descript + table
            embed.set_footer(text="Link: " + topic.link)
            embed.color = 3066993
            await ctx.send(embed=embed)
            await loading.delete()
        except:
            embed = discord.Embed()
            embed.set_author(name="Not Available")
            embed.color = 3066993
            embed.description = (
                "Your Search isn't available, the first link that showed up was: "
                + topic.link
            )
            embed.set_image(
                url="https://i.pinimg.com/236x/3a/52/08/3a52083989b854ab0e72efeb3531f6d3.jpg"
            )
            await ctx.send(embed=embed)
            await loading.delete()


def setup(bot):
    bot.add_cog(CSsearch(bot))


# k = google_query("array", api_key, cse_id, num=1)
# link = k[0]["link"]
# stuff = requests.get(link)
# df_list = pd.read_html(stuff.text)  # this parses all the tables in webpages to a list
# df = df_list[0]
# df = df.iloc[:, :2]
# df.loc[:, ("definition")] = df.definition.apply(
#     lambda x: x.rsplit(maxsplit=len(x.split()) - 3)[0]
# )

# table = df.to_string(index=False)
# k = table.split(" ")

# fl = []
# for stuff in k:
#     fl.append(stuff)
# print(fl[0].get_text()[:400])
# # https://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
# data = []
# table = soup.find("table")
# table_body = table.find("tbody")

# print(table.get_text())


# img = soup.find("img")
# print(img["src"])
