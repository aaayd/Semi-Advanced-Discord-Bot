import discord, re, asyncio
from discord.utils import get
from discord.ext import commands, tasks
from datetime import datetime, timedelta
from colorama import Fore, Style
from main import CLUSTER


MUTE_DB = CLUSTER["discord"]["mute"]
BLACKLIST = CLUSTER["discord"]["utils"].find_one({"id": "type_blacklist"})["blacklist"]



class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        self._mute_db_check.start(self)
        self._spam_risky.start(self)

    def converter(self, time):
        time_converter={
            's': 1,
            'm': 60,
            'h': 3600,
            'd': 86400,
            'w': 604800}

        time = re.sub('[^a-zA-Z]+', '', time)
        return time_converter.get(time,"Invalid Timeframe.")

    @tasks.loop(seconds=10.0)
    async def _mute_db_check(self, ctx):
        time_now = datetime.utcnow()
        guild = self.client.get_guild(787823476966162452)
        for muted_user in MUTE_DB.find({}):
            if time_now > muted_user["end_date"]:
                try:
                    for member in guild.members:
                        if member.id == muted_user["id"]:
                            await self._unmute_user(member)
                            MUTE_DB.delete_many({'id': member.id})
                            print (f"{Fore.BLUE}[-]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.YELLOW}[UNMUTED]{Style.RESET_ALL} {Fore.CYAN}{member}{Style.RESET_ALL} via Database check ")
                            continue
                except:
                    pass

    @tasks.loop(seconds=15.0)
    async def _spam_risky(self, ctx):
        try:          
            channel = self.client.get_channel(808411651921412107)
            guild = self.client.get_guild(787823476966162452)
            for member in guild.members:
                if member.id == 470252232906899466:
                    for role in member.roles:
                        if role.id == 811989775904145479:
                            message = await channel.send(f"{member.mention} Get rid of your developer role.")
        except:
            pass
    
    @commands.Cog.listener()
    async def on_message(self, message):        
        if message.reference is not None and message.channel.id != 822636894377869342 and message.author.id == 506240196036263937:
            x = await message.channel.fetch_message(message.reference.message_id)
            if x.author == message.author:
                await x.delete()
                await message.delete()

                embed = discord.Embed(description=f"Message & Reply deleted!\nFurther instances of this will be a mute as this is considered spam.\nAny avoidance of this will also be considered spam", colour=0xFF0000)
                await message.author.send(embed=embed)

        
        racist = ["nigga"]
        
        try:
            if any(word in message.content.lower() for word in BLACKLIST):
                await message.delete()
            if any(word in message.content.lower() for word in  racist) and "Racist" in [role.name for role in message.author.roles]:
                await message.delete()

        except:
            pass
            
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        '''?kick [member] [reason]'''
        
        #if ctx.author.id == 470252232906899466:
        #    return

        await ctx.message.delete()
        await ctx.channel.trigger_typing()
        log_channel = self.client.get_channel(808411931383431198)
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[KICK]{Style.RESET_ALL} on member {Fore.RED}{member}{Style.RESET_ALL}")
        try:
                
            embed=discord.Embed(title="", description=f" ", timestamp=datetime.utcnow(), color=0xff0000
                ).set_author(name=f"{ctx.author} kicked member", icon_url=f"{ctx.author.avatar_url}"
                ).add_field(name="User", value=f"{member.mention}"
                ).add_field(name="Punishment", value=f"Kicked"
                ).add_field(name="Reason", value=f"{reason}"
            )
            await log_channel.send(embed=embed)
            await member.send(embed=embed)
            await member.kick(reason=reason)

        except:
            pass

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        '''?ban [member] [reason]'''
        #if ctx.author.id == 470252232906899466:
        #    return
                   
        await ctx.message.delete()
        await ctx.channel.trigger_typing() 
        log_channel = self.client.get_channel(808411931383431198)
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[BAN]{Style.RESET_ALL} on member {Fore.RED}{member}{Style.RESET_ALL}")
        try:
            embed=discord.Embed(title="", description=f" ", timestamp=datetime.utcnow(), color=0xff0000
                ).set_author(name=f"{ctx.author} banned member", icon_url=f"{ctx.author.avatar_url}"
                ).add_field(name="User", value=f"{member.mention}"
                ).add_field(name="Punishment", value=f"Banned"
                ).add_field(name="Reason", value=f"{reason}"
            )
            await member.ban(reason=reason)
            await log_channel.send(embed=embed)
            await member.send(embed=embed)
            await member.send("https://cdn.discordapp.com/attachments/811885989005492276/812847731461849108/y2mate.com_-_ARSENAL_FAN_TV_ITS_TIME_TO_GO_MEME_360p_1.mp4")
            
            
            
        except:
            pass


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, member : discord.Member, limit: int=None):
        '''?clear [member] [amount to delete]'''

        await ctx.channel.trigger_typing()
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[CLEAR]{Style.RESET_ALL} on member {Fore.RED}{member}{Style.RESET_ALL}")
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
    async def mute(self, ctx, member : discord.Member, time="Indefinite", *, reason="None"):
        '''?mute [member] [time] [reason]'''

        await ctx.message.delete() 
        await ctx.channel.trigger_typing()
        
        if time.isdigit():
            time = f"{time}m"

        if time.isalpha():
            reason = f"{time} {reason}"
            time = "Indefinite"
        
        if reason == "Indefinite None":
            reason = "None"
        
        if reason[-4:] == "None" and len(reason) != 4:
            reason = reason[:-4]

        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[MUTE]{Style.RESET_ALL} on member {Fore.RED}{member}{Style.RESET_ALL}")        

        
        await self._mute_user(ctx, member, time, reason)   
        
        if time !='Indefinite':
            await self._unmute_user(member)
            MUTE_DB.delete_many({'id': member.id})

    @commands.command()
    @commands.has_guild_permissions(mute_members=True)
    async def unmute(self, ctx, member : discord.Member=None):
        '''?unmute [member]'''


        await ctx.message.delete()
        await ctx.channel.trigger_typing()

        if member == None:
            member = ctx.message.author    
        
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[UNMUTE]{Style.RESET_ALL} on member {Fore.RED}{member}{Style.RESET_ALL}")
        await self._unmute_user(member)
        MUTE_DB.delete_many({'id': member.id})

    async def _mute_user(self, ctx, member, time="Indefinite", reason="None"):
        channel = self.client.get_channel(808466681067470928)
        
        muted_role = get(ctx.guild.roles, id=809969441772929065)
        if muted_role in member.roles:
            return
        
        await member.add_roles(muted_role)
        
        timestr = ""

        if str(time).endswith("d"):
            timestr += f"{str(time)[:-1]} day" if str(time)[:-1] == "1" else f"{str(time)[:-1]} days" 
        elif str(time).endswith("h"):
            timestr += f"{str(time)[:-1]} hour" if str(time)[:-1] == "1" else f"{str(time)[:-1]} hour" 
        elif str(time).endswith("m"):
            timestr += f"{str(time)[:-1]} minute" if str(time)[:-1] == "1" else f"{str(time)[:-1]} minutes" 
        elif str(time).endswith("s"):
            timestr += f"{str(time)[:-1]} second" if str(time)[:-1] == "1" else f"{str(time)[:-1]} seconds" 

        embed=discord.Embed(title="", description=f"Please go to {channel.mention} and explain the reason for muting (staff)", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{ctx.author} muted member", icon_url=f"{ctx.author.avatar_url}"
            ).add_field(name="Muted User", value=f"{member.mention}"
            ).add_field(name="Reason", value=f"{reason}"
            ).add_field(name="Time", value=f"{timestr}"
        )
        try:
            await ctx.send(embed=embed)
        except:
            pass
        
        if time != 'Indefinite':
            time_to_seconds = int(re.findall(r'\d+', str(time))[0]) * self.converter(re.sub('[^a-zA-Z]+', '', time))
            end_date = datetime.utcnow() + timedelta(seconds=time_to_seconds)
            
            greenie = ({"id" : member.id, "end_date": end_date})
            MUTE_DB.insert(greenie)

            await asyncio.sleep(time_to_seconds)

        else:
            await member.add_roles(muted_role)
                                    
    async def _unmute_user(self, member):
        channel = self.client.get_channel(808411931383431198)
        channel1 = self.client.get_channel(787823476966162455)
        muted_role = get(member.guild.roles, id=809969441772929065)
    
        await member.remove_roles(muted_role)

        embed=discord.Embed(title="", description=f" ", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{member} is now unmuted", icon_url=f"{member.avatar_url}"
            ).add_field(name="Unmuted User", value=f"{member.mention}"
        )
        await channel.send(embed=embed)
        await channel1.send(embed=embed)



def setup(client):
    client.add_cog(Moderation(client))
