import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp
import sys
import pandas as pd

pd.options.mode.chained_assignment = None
sys.path.insert(1, "./Api/")
from GoogleApi import google_query
from GoogleApi import api_key
from GoogleApi import cse_id


class Cpp:
    def __init__(self, soup, link):
        self.link = link
        self.soup = soup

    # def testscrapeDescription(self):
    #     D = self.soup.find("section")
    #     return D.get_text()

    def scrapeDescription(self):
        D = self.soup.find("section")
        # D = self.soup.find("a", attrs={"class": "image image-thumbnail"})
        # backward = BeautifulSoup("```", "lxml")
        description = D.get_text()
        if len(D.get_text()) > 499:
            return description[:500] + "..."
        else:
            return description

    def scrapeTable(self):
        df_list = pd.read_html(self.link)
        df = df_list[0]
        if len(df.index) > 1:
            try:
                df = df.iloc[:, :2]
                temp = df.definition.apply(
                    lambda x: x.rsplit(maxsplit=len(x.split()) - 3)[0]
                )
                df.loc[:, ("definition")] = temp
                finalStr = ("```") + df.to_string(index=False) + ("```")
                return finalStr

            except:
                T = self.soup.find("div", attrs={"class": "auto"})
                T = T.find("table")
                table = ("```") + T.get_text() + ("```")
                return table

        else:
            T = self.soup.find("div", attrs={"class": "auto"})
            T = T.find("table")
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
    async def search(self, ctx, *, arx: str):
        """Searches CSV for """
        df = pd.read_csv(
            "https://raw.githubusercontent.com/LastAeon77/CSbot/master/Data/searchCpp.csv"
        )
        df["Name"] = df["Name"].str.lower()
        row = df.loc[df["Name"] == arx.lower()]
        if row:
            embed = discord.Embed()
            embed.set_author(name=row["Name"][0])
            embed.description = (
                row["Description"][0] + row["Code"][0] + row["Result"][0]
            )
            embed.set_image(url=row["Image Link"][0])
            await ctx.send(embed=embed)
        else:
            otherdf = df[df.Name.str[:2].str.lower() == arx[:2].lower()]
            otherdf = otherdf["Name"]
            final_str = ""
            for names in otherdf:
                final_str = final_str + "> " + names + "\n"
            await ctx.send(final_str)

    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(str(url)) as resp:
                if resp.status == 200:
                    return BeautifulSoup(await resp.text(), "lxml")

    @commands.command()
    async def cppReport(self, ctx, *, arx: str):
        """Report commands that you find wrong"""
        with open("./cogs/CppReport.txt", "a") as reporttxt:
            # print(arx + " Has been added")
            reporttxt.write(arx)
        await ctx.send(f"You have reported a problem with: {arx}")

    @commands.command()
    async def cpp(self, ctx, *, arx: str):
        """Searches cplusplus.com for information"""
        loading = await ctx.send("Please wait a moment")
        k = google_query(arx, api_key, cse_id, num=1)
        link = k[0]["link"]
        soup = await self.fetch(link)
        topic = Cpp(soup, link)
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


# df = pd.read_csv(
#     "https://raw.githubusercontent.com/LastAeon77/CSbot/master/Data/searchCpp.csv"
# )
# df["Name"] = df["Name"].str.lower()
# arx = "int"
# row = df.loc[df["Name"] == arx.lower()]
# embed = discord.Embed()
# print(row['Name'][0])
# print(row["Description"][0] + row["Code"][0] + row["Result"][0])
# print(row["Image Link"])
