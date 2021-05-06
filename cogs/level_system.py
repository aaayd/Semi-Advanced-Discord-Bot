import os, discord
from threading import ExceptHookArgs
from discord.enums import NotificationLevel
from discord.ext import commands, tasks
from main import CLUSTER


text_channels = [808411931383431198]
levels = {
    '5': "Level 5",
    '10': "Level 10",
    '15': "Level 15",
    '20': "Level 20"
}
path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image_processing')
leveling = CLUSTER["discord"]["leveling"]
rate_limit = CLUSTER["discord"]["xp_rate_limit"]

class LevelSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._rate_limit_check.start(self)

    @tasks.loop(minutes=1)
    async def _rate_limit_check(self, ctx):
        try:
            rate_limit.delete_many({'rate_limited': True})
        except:
            pass

    @commands.has_role("Developer")
    @commands.command()
    async def _give_xp(self, ctx, xp=500, member : discord.Member = None):
        await ctx.message.delete()
        await ctx.channel.trigger_typing()
        
        if member is None:
            return
            
        stats = leveling.find_one({"id" : member.id})
        _xp = stats["xp"] + xp 
        leveling.update_one({"id": member.id}, {"$set":{"xp":_xp}})
                

    @commands.has_role("Developer")
    @commands.command()
    async def _round_xp(self, ctx, mod_div=5):
        await ctx.message.delete()
        for member in ctx.guild.members:
            stats = leveling.find_one({"id" : member.id})
            if stats is None:
                continue

            xp = stats["xp"]

            if xp % 5 != 0:
                xp = mod_div * round(xp/mod_div)
            
            leveling.update_one({"id": member.id}, {"$set":{"xp":xp}})
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel) or message.channel.id == 822636894377869342:
            return
        
        if message.channel.id != 787823476966162455:
            return
            
        _rate_limit = rate_limit.find_one({"id" : message.author.id})
        if message.author.id != 257254775530323968:
            if _rate_limit is None:
                _rl_user = ({"id" : message.author.id, "rate_limited": True})
                rate_limit.insert(_rl_user)

            else:
                return


        if not message.author.bot:
            stats = leveling.find_one({"id" : message.author.id})
            if stats is None:
                greenie = ({"id" : message.author.id, "xp": 0, 
                            "username": f"{str(message.author.name)}#{str(message.author.discriminator)}",
                            "av_url": str(message.author.avatar_url)
                })

                leveling.insert(greenie)
            
            else:
                xp = stats["xp"] + 5

                username = f"{str(message.author.name)}#{str(message.author.discriminator)}"
                leveling.update_one({"id": message.author.id}, {"$set":{"xp":xp}})
                leveling.update_one({"id": message.author.id}, {"$set":{"username":username}})
                leveling.update_one({"id": message.author.id}, {"$set":{"av_url":str(message.author.avatar_url)}})
                lvl = 0

                while True:
                    if xp < ((50*(lvl**2))+(50*(lvl-1))):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                if xp == 0:
                    try:
                        if str(lvl) in levels:
                            embed = discord.Embed(description=f"You talk a lot {message.author.mention}. Look at your shit level {lvl}"
                                ).set_image(url="https://i.imgur.com/qgpcufH.gif"
                            )
                            await message.channel.send(embed=embed)
                            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name = levels.get(str(lvl))))
                    except:
                        pass

                
    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        '''?leaderboard'''
        await ctx.message.delete()
        embed = discord.Embed(description=f"The leaderboard has migrated to the internet!\nClick [here](http://cache-discord.tech/) to view the server [leaderboard](http://cache-discord.tech/)")
        await ctx.send(embed=embed)
        
    
def setup(client):
    client.add_cog(LevelSystem(client))
