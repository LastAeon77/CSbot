async def owner_check(ctx):
    return ctx.author.id == ctx.bot.config["discord"]["owner"]


async def member_check(ctx):
    return (
        ctx.author.id == ctx.bot.config["Allowed_Users"]["member1"]
        or ctx.author.id == ctx.bot.config["discord"]["owner"]
    )
