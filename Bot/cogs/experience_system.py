from Bot.utils.error_handler import ExpectedLiteralInt, MissingArgument, NotInDatabase, embed_error, embed_success
from Bot.utils.constants import IMAGE_PATH, command_activity_check, get_channel_id, get_cluster, get_command_description, get_level, get_rank
from Bot.cogs.image_manipulation import create_rank_card
import discord, os
from discord.ext import commands

class ExperienceSystem(commands.Cog, name = "XP Commands"):
    """
    Rank and Leveling related commands.
    """
    def __init__(self, bot):
        self.bot = bot
        #self._rate_limit_check.start(self)

    """
    TODO
    @tasks.loop(minutes=1)
    async def _rate_limit_check(self, ctx):
        try:
            CLUSTER_RATELIMIT.delete_many({'rate_limited': True})
        except:
            pass
    """
        

    @commands.command(name="rank", aliases=["level"], description="Sends an image of [member]'s rank card")
    @command_activity_check()
    async def _rank(self, ctx, member: discord.Member = None):
        f"""
        {self.bot.command_prefix}{ctx.command.name} <member>
        """
        
        await ctx.message.delete()
          
        if member is None:
            member = ctx.author

        _db = get_cluster(ctx.message.guild.id, "CLUSTER_EXPERIENCE")


        await ctx.channel.trigger_typing()
        
        stats = _db.find_one({
            "id" : member.id
        })

        if stats is None:
            raise NotInDatabase(member, "experience")

        xp = stats["xp"]
        lvl = get_level(xp)
        xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
        rank = get_rank(member, _db)

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

    @commands.command(name="leaderboard", aliases=["lb"], description="Sends an image of [placement number]'s rank card")
    @command_activity_check()
    async def _leaderboard(self, ctx, placement = None):
        f"""
        {self.bot.command_prefix}{ctx.command.name} <number>
        """
        
        await ctx.message.delete()
          
        if placement is None:
            raise MissingArgument("Placement number", get_command_description(ctx.command.name))

        try:
            placement = int(placement)
        except:
            raise ExpectedLiteralInt

        _db = get_cluster(ctx.message.guild.id, "CLUSTER_EXPERIENCE")


        await ctx.channel.trigger_typing()
        
        stats = _db.find().sort("xp", -1)

        for i, stat in enumerate(list(stats)):
            if (i + 1) == placement:
                stats = stat
                break
        
        try:
            xp = stats["xp"]
            lvl = get_level(xp)
            xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
            rank = placement
            member = discord.utils.get(self.bot.get_all_members(), id=stats["id"])
        except:
            await ctx.send(embed=embed_error(f"Member in place `{placement}` has no XP"))
            return

        try:
            colour = (stats["colour"][0],stats["colour"][1],stats["colour"][2])
        except KeyError:
            colour = (65, 178, 138)

        try:
            background = (stats["background"])
        except KeyError:
            background = "https://media.discordapp.net/attachments/665771066085474346/821993295310749716/statementofsolidarity.jpg?width=1617&height=910"
    
        
        try:
            create_rank_card(member, xp, lvl, rank, background, colour, ctx.guild.member_count)
            await ctx.send(file=discord.File(os.path.join(f"{IMAGE_PATH}//temp//","card_temp.png")))
        except:
            await ctx.send(embed=embed_error("That user is no longer in the server"))

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.channel.DMChannel):
            return
        
        channel = self.bot.get_channel(get_channel_id(message.guild.id, "channel_general"))

        if channel != message.channel:
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

def setup(bot):
    bot.add_cog(ExperienceSystem(bot))
