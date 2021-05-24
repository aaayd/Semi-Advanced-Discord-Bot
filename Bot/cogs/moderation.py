from Bot.utils.error_handler import MissingArgument, MissingPermissionOnMember
import discord, re, asyncio
from discord.utils import get
from datetime import datetime
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from Bot.utils.constants import ALL_GUILD_DATABASES, command_activity_check, converter, get_channel_id, get_cluster, get_command_description


class Moderation(commands.Cog, name = "Moderation Commands"):
    """
    Moderation related commands.
    """

    def __init__(self, client):
        self.client = client
        self.muted_members_check.start(self)

    
    @tasks.loop(seconds=3)
    async def muted_members_check(self, ctx):
        await self.client.wait_until_ready()

        time_now = datetime.utcnow()

        for guild_id, value in ALL_GUILD_DATABASES.items():
            muted_collection = [db for db in value if db == "mute"]

            if muted_collection:
                _db = get_cluster(guild_id, "CLUSTER_MUTE")

                for muted_user in _db.find({}):
                    if time_now > muted_user["end_date"]:
                        member = discord.utils.get(self.client.get_all_members(), id=muted_user["id"])
                        try:
                            await self._unmute_user(member)
                            _db.delete_many({'id': int(member.id)})

                        except (TypeError, AttributeError) as e:
                            # Bot not initiated
                            pass
                        
            
    @commands.command(name="kick", description="Kick a member")
    @command_activity_check()
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, member : discord.Member = None, *, reason=None):
        f"""
        {self.client.command_prefix}{ctx.command.name} <member> <reason>
        """
        
        if member is None:
            raise MissingArgument("Discord User", get_command_description(ctx.command.name))

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
        

    @commands.command(name="ban", description="Ban a member")
    @command_activity_check()
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, member : discord.Member = None, *, reason=None):
        f"""
        {self.client.command_prefix}{ctx.command.name} <member> <reason>
        """

        if member is None:
            raise MissingArgument("Discord User", get_command_description(ctx.command.name))

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
    
        
    @commands.command(name="clear", description="Clear messages by a user")
    @command_activity_check()
    @commands.has_permissions(manage_messages=True)
    async def _clear(self, ctx, member : discord.Member = None, limit: int=None):
        f"""
        {self.client.command_prefix}{ctx.command.name} <member> <amount to delete>
        """

        if member is None:
            raise MissingArgument("Discord User", get_command_description(ctx.command.name))

        await ctx.channel.trigger_typing()
        channel_arr = [channel for channel in ctx.guild.text_channels]
        for channel in channel_arr:
            async for message in channel.history(limit=limit):
                if message.author == member:
                    try:
                        await message.delete()
                    except:
                        pass

    @commands.command(name="mute", description="Mute a user")
    @command_activity_check()
    @commands.has_guild_permissions(mute_members=True)
    async def _mute(self, ctx, member : discord.Member = None, time="Indefinite", *, reason="None"):
        f"""
        {self.client.command_prefix}{ctx.command.name} <member> <time> <reason>
        """

        if member is None:
            raise MissingArgument("Discord User", get_command_description(ctx.command.name))


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

    @commands.command(name="warn", description="Warn a user")
    @command_activity_check()
    @commands.has_guild_permissions(mute_members=True)
    async def _warn(self, ctx, member : discord.Member, reason = None):
        f"""
        {self.client.command_prefix}{ctx.command.name} <member> <reason>
        """
        
        _db = get_cluster(ctx.guild.id, "CLUSTER_WARN")
        
        new_warn = ({
                    "warned_user_name" : str(member), 
                    "warned_user_id": member.id,
                    "warn_reason" : reason,
                    "moderator_name" : str(ctx.author),
                    "moderator_id" : ctx.author.id,
                    "time" : datetime.utcnow()
                })

        _db.insert(new_warn)
        
        embed=discord.Embed(title="", description=f" ", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{ctx.author} warned a user", icon_url=f"{ctx.author.avatar_url}"
            ).add_field(name="Warned User", value=f"{member.mention}"
            ).add_field(name="Reason", value=f"{reason}"
        )
        
        log_channel = self.client.get_channel(get_channel_id(member.guild.id, "channel_logs"))
        await log_channel.send(embed=embed)
        await ctx.channel.send(embed=embed)
        
    @commands.command(name="modlogs", aliases=["warns", "modlog"], description="View a user's warns")
    @command_activity_check()
    @commands.has_guild_permissions(mute_members=True)
    async def _modlogs(self, ctx, member : discord.Member):
        f"""
        {self.client.command_prefix}{ctx.command.name} <member>
        """
        _db = get_cluster(ctx.guild.id, "CLUSTER_WARN").find({"warned_user_id" : member.id})

        embed=discord.Embed(title="", description=f" ", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{member}'s' warns", icon_url=f"{member.avatar_url}"
        )

        for i, warn in enumerate(_db):
            embed.add_field(name=f"Warn {i+1}: {warn['moderator_name']}", value=warn["warn_reason"], inline=False)
        
        await ctx.channel.send(embed=embed)


    @commands.command(name="unmute", description="Unmute a user")
    @command_activity_check()
    @commands.has_guild_permissions(mute_members=True)
    async def _unmute(self, ctx, member : discord.Member=None):
        f"""
        {self.client.command_prefix}{ctx.command.name} <member>
        """


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
            await ctx.message.guild.create_role(name="Muted", colour=0x505050)

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
        try:
            channel1 = self.client.get_channel(get_channel_id(member.guild.id, "channel_logs"))
        
            
            muted_role = get(member.guild.roles, name="Muted")
            await member.remove_roles(muted_role)
            embed=discord.Embed(
                description=f" ", 
                timestamp=datetime.utcnow(), 
                color=0xff0000
                ).set_author(name=f"{member} is now unmuted", icon_url=f"{member.avatar_url}"
                ).add_field(name="Unmuted User", value=f"{member.mention}"
            )
            await channel1.send(embed=embed)
        except:
            pass



def setup(client):
    client.add_cog(Moderation(client))