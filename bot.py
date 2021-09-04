# ID of the channel you want to have proxies in.
channel_id = 883789010529574943


from discord.ext import commands
import requests, asyncio, time, re, discord

bot = commands.Bot(command_prefix="-")

@bot.event
async def on_ready():
    print("bot online")

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Response Times", description="Loading...")
    time_before = time.time()
    edit = await ctx.send(embed=embed, content=f"{ctx.author.mention}")
    time_after = time.time()
    difference = int((time_after - time_before) * 1000)
    embed = discord.Embed(title="Response Times", colour=discord.Color.green())
    embed.add_field(name="API", value=f"`{difference}ms`")
    embed.add_field(name="Websocket", value=f"`{int(bot.latency * 1000)}ms`")
    await edit.edit(embed=embed, content=f"{ctx.author.mention}")

async def setup():
    await bot.wait_until_ready()
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="-ping | Code for me on GitHub!"))
    channel = bot.get_channel(channel_id)
    message = None
    while channel != None:
        req = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all")
        ip = re.findall( r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})', req.text)
        with open("socks4.txt", "w") as f:
            for x in ip:
                f.write(f"{x}\n")
        req = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all")
        ip = re.findall( r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})', req.text)
        with open("socks5.txt", "w") as f:
            for x in ip:
                f.write(f"{x}\n")
        req = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
        ip = re.findall( r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4})', req.text)
        with open("http(s).txt", "w") as f:
            for x in ip:
                f.write(f"{x}\n")
        my_files = [
            discord.File('socks4.txt'),
            discord.File('socks5.txt'),
            discord.File('http(s).txt'),
        ]
        if message == None:
            message = await channel.send(content=f"Proxies from ProxyScape, updated every 5 mins.\nLast updated at <t:{int(time.time())}:R>", files=my_files)
        else:
            await message.delete()
            message = await channel.send(content=f"Proxies from ProxyScape, updated every 5 mins.\nLast updated at <t:{int(time.time())}:R>", files=my_files)
        await asyncio.sleep(300)

bot.loop.create_task(setup())
bot.run("ODgzNzk3NDQwOTE3MDMzMDIy.YTPKgg.oS3P6kxgQKkwhYMbBe2qAgEomIo")