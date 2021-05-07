from utils.constant_strings import IMAGE_PATH
from cogs.image_manipulation import create_rank_card
import discord, os
from discord.ext import commands
from utils.clusters import CLUSTER_EXPERIENCE

class ExperienceSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

        
    def _get_level(self, xp):
        lvl = 0
        while True:
            if xp < ((50*(lvl**2))+(50*(lvl))):
                break
            lvl += 1
        return lvl

    def _get_rank(self, member):
        rankings = CLUSTER_EXPERIENCE.find().sort("xp", -1)
        for iter,rank in enumerate(list(rankings)):
            if rank["id"] == member.id:
                return iter + 1

    @commands.command(aliases=["rank"])
    async def _rank(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        
        if member is None:
            member = ctx.author


        await ctx.channel.trigger_typing()
        
        stats = CLUSTER_EXPERIENCE.find_one({
            "id" : member.id
        })

        if stats is None:
            await ctx.send("This user has no XP")
            return

        xp = stats["xp"]
        lvl = self._get_level(xp)
        xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
        rank = self._get_rank(member)

        try:
            colour = (stats["colour"][0],stats["colour"][1],stats["colour"][2])
        except KeyError:
            colour = (65, 178, 138)

        try:
            background = (stats["background"])
        except KeyError:
            background = "https://media.discordapp.net/attachments/665771066085474346/821993295310749716/statementofsolidarity.jpg?width=1617&height=910"

        create_rank_card(member, xp, lvl, rank, background, colour, ctx.guild.member_count)
        await ctx.send(file=discord.File(os.path.join(f"{IMAGE_PATH}//temp//","card_temp.png")))
    
def setup(client):
    client.add_cog(ExperienceSystem(client))