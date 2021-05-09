from utils.constants import CLUSTER_RATELIMIT, IMAGE_PATH, get_cluster
from cogs.image_manipulation import create_rank_card
import discord, os
from discord.ext import tasks   
from discord.ext import commands

class ExperienceSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
        self._rate_limit_check.start(self)

    @tasks.loop(minutes=1)
    async def _rate_limit_check(self, ctx):
        try:
            CLUSTER_RATELIMIT.delete_many({'rate_limited': True})
        except:
            pass

        
    def _get_level(self, xp):
        lvl = 0
        while True:
            if xp < ((50*(lvl**2))+(50*(lvl))):
                break
            lvl += 1
        return lvl

    def _get_rank(self, member, _db):
        rankings = _db.find().sort("xp", -1)
        for iter,rank in enumerate(list(rankings)):
            if rank["id"] == member.id:
                return iter + 1

    @commands.command(aliases=["rank"])
    async def _rank(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        
        _db = get_cluster(ctx.message.guild.id, "CLUSTER_EXPERIENCE")

        if member is None:
            member = ctx.author


        await ctx.channel.trigger_typing()
        
        stats = _db.find_one({
            "id" : member.id
        })

        if stats is None:
            await ctx.send("This user has no XP")
            return

        xp = stats["xp"]
        lvl = self._get_level(xp)
        xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
        rank = self._get_rank(member, _db)

        try:
            colour = (stats["colour"][0],stats["colour"][1],stats["colour"][2])
        except KeyError:
            colour = (65, 178, 138)

        try:
            background = (stats["background"])
        except KeyError:
            background = "https://media.discordapp.net/attachments/665771066085474346/821993295310749716/statementofsolidarity.jpg?width=1617&height=910"
       
        await ctx.send(xp)
        create_rank_card(member, xp, lvl, rank, background, colour, ctx.guild.member_count)
        await ctx.send(file=discord.File(os.path.join(f"{IMAGE_PATH}//temp//","card_temp.png")))

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            return

        if not message.author.bot:
            _db = get_cluster(message.guild.id, "CLUSTER_EXPERIENCE")
            stats = _db.find_one({"id" : message.author.id})
            if stats is None:
                greenie = ({
                    "id" : message.author.id, 
                    "xp": 5, 
                })

                _db.insert(greenie)
            
            else:
                xp = stats["xp"] + 5
                lvl = 0
                _db.update_one({"id": message.author.id}, {"$set":{"xp":xp}})

                while True:
                    if xp < ((50*(lvl**2))+(50*(lvl-1))):
                        break
                    lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                
                if xp == 0:
                    embed = discord.Embed(
                        description=f"{message.author.mention} Reached Level {lvl}!"
                        ).set_image(url="https://i.imgur.com/qgpcufH.gif"
                    )

                    await message.channel.send(embed=embed)

def setup(client):
    client.add_cog(ExperienceSystem(client))