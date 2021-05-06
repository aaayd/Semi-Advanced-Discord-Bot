import praw, random, requests, discord
from requests.exceptions import HTTPError
from discord.ext import commands

r = praw.Reddit(client_id="7oE7yB5GJJua2Q", client_secret="ooidPB-ETJxbRflpja6a65KX03g", user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36', username="PhantomVipermon", check_for_async=False)

class NSFW(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hentai(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit("hentai")
            #posts = [post for post in sub.hot(limit=50)]
            #random_post_number = random.randint(0, 50)
            #random_post = posts[random_post_number]
            #await ctx.send(random_post.url)

            embed=discord.Embed(title="", description=f"Here is hentai", inline=False).set_image(url=f"{sub.random().url}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("U can't use that command here!")

    @commands.command(aliases=["butt"])
    async def ass(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit('buttplug')

            embed=discord.Embed(title="", description=f"Here is some ass", inline=False).set_image(url=f"{sub.random().url}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("U can't use that command here!")

    @commands.command(aliases=["tit", "boobs"])
    async def tits(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit('boobs')
            embed=discord.Embed(title="", description=f"Here are some tits", inline=False).set_image(url=f"{sub.random().url}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("U can't use that command here!")

    @commands.command()
    async def feet(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit('ButtsAndBareFeet')
            embed=discord.Embed(title="", description=f"Here are some feet", inline=False).set_image(url=f"{sub.random().url}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("U can't use that command here!")

    @commands.command(aliases=["dickpic"])
    async def cock(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit('DickPics4Freedom')

            embed=discord.Embed(title="", description=f"Here is some a dick", inline=False).set_image(url=f"{sub.random().url}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("U can't use that command here!")

    @commands.command()
    async def gaygif(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit('gaygifs')
            await ctx.send(sub.random().url)
        else:
            await ctx.send("U can't use that command here!")

    @commands.command()
    async def porngif(self, ctx):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            sub = r.subreddit('porngifs')
            await ctx.send(sub.random().url)
        else:
            await ctx.send("U can't use that command here!")

    @commands.command()
    async def r34(self, ctx, *arg):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            if len(arg) > 0:
                try:
                    string = '+'.join(map(str,arg))
                    string = "https://r34-json-api.herokuapp.com/posts?tags="+string

                    response = requests.get(str(string))
                    response.raise_for_status()
                    # access JSOn content
                    jsonResponse = response.json()
                    jsonlen = len(jsonResponse)
                    if jsonlen > 0:
                        image = jsonResponse[random.randint(0,jsonlen-1)]["file_url"]
                        embed=discord.Embed(title="", description=f"Here is {( ' '.join(arg))} rule 34", inline=False).set_image(url=f"{image[46:]}")
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send("no results for search: '" + ' '.join(map(str,arg)) + "' in rule34.xxx")

                except HTTPError as http_err:
                    await ctx.send(f'HTTP error occurred: {http_err}')
                except Exception as err:
                    await ctx.send(f'Other error occurred: {err}')
            else:
                await ctx.send("you need to give at least 1 argument")
        else:
            await ctx.send("U can't use that command here!")

    @commands.command()
    async def reddit(self, ctx, *args):

        if hasattr(ctx.message.channel, "nsfw"):
            channel_nsfw = ctx.message.channel.nsfw
        else:
            channel_nsfw = str(ctx.message.channel.type) == "private"

        if channel_nsfw:
            if len(args) > 0:
                print(args[0])
                sub = r.subreddit(args[0])
                try:
                    embed=discord.Embed(title="", description=f"Here is the reddit post", inline=False).set_image(url=f"{sub.random().url}")
                    await ctx.send(embed=embed)
                except Exception as err:
                    await ctx.send("subreddit don't have random post enabled or doesn't exist")
            else:
                await ctx.send("you need to give at least 1 argument")
        else:
            await ctx.send("U can't use that command here!")

def setup(client):
    client.add_cog(NSFW(client))
