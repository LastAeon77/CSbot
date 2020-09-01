from discord.ext import commands
import discord
from discord.utils import get
from utils.checks import member_check
import random

random.seed()


class CSRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.check(owner_check)
    # @commands.command()
    # async def member(self, ctx):
    #     x = ctx.guild.members
    #     for member in x:
    #         for role in member.roles:
    #             print(role)

    # @commands.check(member_check)
    # @commands.command()
    # async def removeRoles(self, ctx, roles):
    #     """Remove certain roles completely"""
    #     x = ctx.guild.members
    #     # roleName = get(ctx.message.guild.roles, name=roles)
    #     for member in x:
    #         for role in member.roles:
    #             if roles == str(role):
    #                 await member.remove_roles(role)

    @commands.check(member_check)
    @commands.command()
    async def assignRolestoSection(self, ctx, k):
        """Type in like this: c!assignRolestoSection <section>,<Group of>"""
        random.seed()
        sampleRole = []
        x = ctx.guild.members
        count = 0
        lol = k.split(",")
        sectionrole = lol[0]
        groupOf = lol[1]
        numberOfPeopleInRole = await self.roleCount(ctx, sectionrole)
        number_of_group = numberOfPeopleInRole // int(groupOf)
        leftover = numberOfPeopleInRole % int(groupOf)
        for i in range(number_of_group):
            for xd in range(int(groupOf)):
                sampleRole.append(f"g{i+1}")
        for i in range(leftover):
            sampleRole.append(f"g{number_of_group+1}")
        # sectionR = get(ctx.message.guild.roles, name=sectionrole)
        random.shuffle(sampleRole)
        print(sampleRole)
        for member in x:
            for role in member.roles:
                if sectionrole == str(role):
                    g = get(ctx.message.guild.roles, name=sampleRole[count])
                    await member.add_roles(g)
                    count += 1
        await self.distributeVC(ctx)
        await ctx.send(
            f"Succesful, everyone from {sectionrole} has been distributed accordingly"
        )

    @commands.check(member_check)
    @commands.command()
    async def backToMain(self, ctx, sectionrole):
        """Removes group role"""
        await self.backtoMainVC(ctx)
        x = ctx.guild.members
        for member in x:
            for r in member.roles:
                if r.name[0] == "g":
                    await member.remove_roles(r)
                # if str(r) != sectionrole:
                #     await member.remove_roles(str(r))
        await ctx.send(f"Every member in {sectionrole} has been brought back")

    @commands.check(member_check)
    @commands.command()
    async def getmember(self, ctx, member: discord.Member):
        print(type(member))
        print(member)

    async def roleCount(self, ctx, rolename):
        cnt = 0
        for member in ctx.guild.members:
            for role in member.roles:
                if role.name == rolename:
                    cnt += 1
        return cnt

    async def distributeVC(self, ctx):
        # Move stuff from Main class vc to other
        Main_Class_Channel = get(
            ctx.message.guild.channels,
            name="Main_Class",
            type=discord.ChannelType.voice,
        )
        for member in Main_Class_Channel.members:
            for roles in member.roles:
                for i in range(10):
                    if roles.name == f"g{i+1}":
                        await member.move_to(await self.vcName(ctx, f"g{i+1}"))
                        break

    async def vcName(self, ctx, vcname):
        voice_channel = discord.utils.get(
            ctx.message.guild.channels,
            name=vcname,
            type=discord.ChannelType.voice,
        )
        return voice_channel

    async def backtoMainVC(self, ctx, arg="Main_Class"):
        for i in range(10):
            Gs = get(
                ctx.message.guild.channels,
                name=f"g{+1}",
                type=discord.ChannelType.voice,
            )
            for member in Gs.members:
                await member.move_to(await self.vcName(ctx, arg))

    # @commands.check(owner_check)
    # @commands.command()
    # async def temp(self, ctx, user: discord.Member):
    #     g = get(ctx.message.guild.roles, name="BotAdmin")
    #     await user.add_roles(g)


def setup(bot):
    bot.add_cog(CSRoles(bot))
