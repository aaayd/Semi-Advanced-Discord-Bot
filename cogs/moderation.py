from utils.error_handler import MissingArgument, MissingPermissionOnMember, embed_error
import discord, re, asyncio
from discord.utils import get
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from utils.constants import converter, get_channel_id, get_cluster, get_command_description


class Moderation(commands.Cog):
    """
    Moderation related commands.
    """

    def __init__(self, client):
        self.client = client
        self._mute_db_check.start(self)

    
    @tasks.loop(seconds=10.0)
    async def _mute_db_check(self, ctx):
        _db = get_cluster(ctx.guild.id, "CLUSTER_MUTE")
        time_now = datetime.utcnow()
        for muted_user in _db.find({}):
            if time_now > muted_user["end_date"]:
                try:
                    member = get(self.client.get_all_members(), id=muted_user["id"])
                    await self._unmute_user(member)
                    _db.delete_many({'id': int(member.id)})
                except:
                    pass
            
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member = None, *, reason=None):
        '''?kick [member] [reason]'''
        
        if member is None:
            raise MissingArgument("Discord User", get_command_description("kick"))

        try:
            await member.kick(reason=reason)
        except:
            raise MissingPermissionOnMember("kick", member)

        await ctx.message.delete()
        await ctx.channel.trigger_typing()
        log_channel = self.client.get_channel(get_channel_id(member.guild.id, "channel_logs"))
                        
        embed=discord.Embed(title="", description=f" ", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{ctx.author} kicked member", icon_url=f"{ctx.author.avatar_url}"
            ).add_field(name="User", value=f"{member.mention}"
            ).add_field(name="Punishment", value=f"Kicked"
            ).add_field(name="Reason", value=f"{reason}"
        )
        await log_channel.send(embed=embed)
        await member.send(embed=embed)
        

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member = None, *, reason=None):
        '''?ban [member] [reason]'''

        if member is None:
            raise MissingArgument("Discord User", get_command_description("ban"))

        try:
            await member.ban(reason=reason)
        except:
            raise MissingPermissionOnMember("ban", member)

        await ctx.message.delete()
        await ctx.channel.trigger_typing()
        log_channel = self.client.get_channel(get_channel_id(member.guild.id, "channel_logs"))
        embed=discord.Embed(
            description=f" ", 
            timestamp=datetime.utcnow(), 
            color=0xff0000
            ).set_author(name=f"{ctx.author} banned member", icon_url=f"{ctx.author.avatar_url}"
            ).add_field(name="User", value=f"{member.mention}"
            ).add_field(name="Punishment", value=f"Banned"
            ).add_field(name="Reason", value=f"{reason}"
        )
        
        await log_channel.send(embed=embed)
        await member.send(embed=embed)
        await member.send("https://cdn.discordapp.com/attachments/811885989005492276/812847731461849108/y2mate.com_-_ARSENAL_FAN_TV_ITS_TIME_TO_GO_MEME_360p_1.mp4")
    
        
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, member : discord.Member = None, limit: int=None):
        '''?clear [member] [amount to delete]'''

        if member is None:
            raise MissingArgument("Discord User", get_command_description("clear"))

        await ctx.channel.trigger_typing()
        channel_arr = [channel for channel in ctx.guild.text_channels]
        for channel in channel_arr:
            async for message in channel.history(limit=limit):
                if message.author == member:
                    try:
                        await message.delete()
                    except:
                        pass

    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def mute(self, ctx, member : discord.Member = None, time="Indefinite", *, reason="None"):
        '''?mute [member] [time] [reason]'''

        if member is None:
            raise MissingArgument("Discord User", get_command_description("mute"))


        await ctx.message.delete() 
        await ctx.channel.trigger_typing()
        
        _db = get_cluster(ctx.guild.id, "CLUSTER_MUTE")

        if time.isdigit():
            time = f"{time}m"

        if time.isalpha():
            reason = f"{time} {reason}"
            time = "Indefinite"
        
        if reason == "Indefinite None":
            reason = "None"
        
        if reason[-4:] == "None" and len(reason) != 4:
            reason = reason[:-4]
        
        await self._mute_user(ctx, member, time, reason)   
        
        if time !='Indefinite':
            await self._unmute_user(member)
            _db.delete_many({'id': member.id})

    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, member : discord.Member=None):
        '''?unmute [member]'''


        await ctx.message.delete()
        await ctx.channel.trigger_typing()

        _db = get_cluster(ctx.guild.id, "CLUSTER_MUTE")

        if member == None:
            member = ctx.message.author    
        
        await self._unmute_user(member)
        _db.delete_many({'id': member.id})

    async def _mute_user(self, ctx, member, time="Indefinite", reason="None"):
        channel = self.client.get_channel(get_channel_id(member.guild.id, "channel_logs"))
        
        try:
            muted_role = get(ctx.guild.roles, name="Muted")
        except:
            await ctx.send(embed=embed_error("Muted Role doesn't exist!"))

        if muted_role in member.roles:
            return
        
        await member.add_roles(muted_role)
        
        timestr = ""

        if str(time).endswith("d") : timestr += f"{str(time)[:-1]} day" if str(time)[:-1] == "1" else f"{str(time)[:-1]} days" 
        elif str(time).endswith("h") :timestr += f"{str(time)[:-1]} hour" if str(time)[:-1] == "1" else f"{str(time)[:-1]} hour" 
        elif str(time).endswith("m") : timestr += f"{str(time)[:-1]} minute" if str(time)[:-1] == "1" else f"{str(time)[:-1]} minutes" 
        elif str(time).endswith("s") : timestr += f"{str(time)[:-1]} second" if str(time)[:-1] == "1" else f"{str(time)[:-1]} seconds" 

        embed=discord.Embed(
            description=f" ",
            timestamp=datetime.utcnow(), 
            color=0xff0000
            ).set_author(name=f"{ctx.author} muted member", icon_url=f"{ctx.author.avatar_url}"
            ).add_field(name="Muted User", value=f"{member.mention}"
            ).add_field(name="Reason", value=f"{reason}"
            ).add_field(name="Time", value=f"{timestr}"
        )
        
        await ctx.send(embed=embed)
        
        if time != 'Indefinite':
            time_to_seconds = int(re.findall(r'\d+', str(time))[0]) * converter(re.sub('[^a-zA-Z]+', '', time))
            end_date = datetime.utcnow() + timedelta(seconds=time_to_seconds)
            _db = get_cluster(ctx.guild.id, "CLUSTER_MUTE")
            greenie = ({"id" : member.id, "end_date": end_date})
            _db.insert(greenie)

            await asyncio.sleep(time_to_seconds)

        else:
            await member.add_roles(muted_role)
                                    
    async def _unmute_user(self, member):
        channel = self.client.get_channel(self.client.get_channel(get_channel_id(member.guild.id, "channel_general")))
        channel1 = self.client.get_channel(self.client.get_channel(get_channel_id(member.guild.id, "channel_logs")))
        
        muted_role = get(member.guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        embed=discord.Embed(
            description=f" ", 
            timestamp=datetime.utcnow(), 
            color=0xff0000
            ).set_author(name=f"{member} is now unmuted", icon_url=f"{member.avatar_url}"
            ).add_field(name="Unmuted User", value=f"{member.mention}"
        )
        await channel.send(embed=embed)
        await channel1.send(embed=embed)



def setup(client):
    client.add_cog(Moderation(client))