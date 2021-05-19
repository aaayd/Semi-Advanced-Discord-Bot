
import discord
from discord.ext import commands
from datetime import datetime
from main import CLUSTER
from Bot.utils.constants import get_cluster, get_time_elapsed

class AFKSystem(commands.Cog):
    """
    AFK Related Commands
    """
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def afk(self, ctx, *, status="No status"):
        """?afk [afk message]"""
        
        await ctx.channel.trigger_typing()
        _db = get_cluster(ctx.message.guild.id, "CLUSTER_AFK")
        find_user = _db.find_one({"id" : ctx.author.id})
        if find_user is None:
            _db.insert({
                "id" : ctx.author.id, 
                "status": status, 
                "date": datetime.utcnow()}
            )
            
            embed=discord.Embed(
                description=f"**Status**: {status}", 
                timestamp=datetime.utcnow(), 
                color=0x800080
                ).set_author(name=f"{ctx.author} is now afk!", icon_url=f"{ctx.author.avatar_url}"
            )

            await ctx.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        _db = get_cluster(message.guild.id, "CLUSTER_AFK")
        for member in message.mentions: 
            find_user = _db.find_one({"id" : member.id})

            if find_user is None or "?afk" in message.content.lower():
                return

            user_id = find_user["id"] 
            afk_status = find_user["status"]  
            afk_date = find_user["date"]
            
            time_afk = get_time_elapsed(afk_date)
            member_obj = await self.client.fetch_user(int(user_id))  
            if str(user_id) in message.content and message.author.id != user_id:
            
                embed=discord.Embed(
                    description=f"This user is AFK! Please wait for them to return", 
                    timestamp=datetime.utcnow(), 
                    color=0x800080
                    ).set_author(name=f"{member_obj}", icon_url=f"{member_obj.avatar_url}"
                    ).add_field(name="AFK Status", value=f"{afk_status}"
                    ).add_field(name="Time AFK", value=f"{time_afk}"
                )
                await message.channel.send(embed=embed)
                return
        
        find_user = _db.find_one({"id" : message.author.id})
        if find_user is not None:
            _db.delete_many({"id" : message.author.id})
            
            embed=discord.Embed(
                description=f"{message.author} is no longer AFK after {get_time_elapsed(find_user['date'])}!", 
                timestamp=datetime.utcnow(), 
                color=0x800080
                ).set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}"
            )
            await message.channel.send(embed=embed)
    
def setup(bot):
    bot.add_cog(AFKSystem(bot))
            