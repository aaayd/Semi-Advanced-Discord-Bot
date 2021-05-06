import discord
from discord.ext import commands
from datetime import datetime
from colorama import Fore, Style
from main import CLUSTER

warn_db = CLUSTER["discord"]["warns"]

class WarnSystem(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['cwarn', 'cleawarn','cwarns'])
    async def clearwarns(self, ctx, member : discord.Member):
        if ctx.author.id == member.id:
            await ctx.send("You cannot use this command on yourself.")
            return

        '''?clearwarns [member]'''
        await ctx.message.delete()
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[CLEAR WARNS]{Style.RESET_ALL} on member {Fore.RED}{member}{Style.RESET_ALL}")
        
        embed = discord.Embed(title="", description=" ", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{ctx.author} removed all warns for {member}", icon_url=f"{ctx.author.avatar_url}"
        )
        warn_db.delete_many({'id': member.id})

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def warn(self, ctx, member : discord.Member, *, reason="No reason"):
        '''?warn [member] [reason]'''
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[WARN]{Style.RESET_ALL} on member {Fore.RED}{member}{Style.RESET_ALL}")
        #if ctx.author.id == 470252232906899466:
        #    return
        await ctx.message.delete()

        if member.id == 483726075269218326:
            await ctx.channel.send(f"Come off my screen {ctx.author.mention}? Stop warning Dripper.")
            return

        find_user = warn_db.find_one({"id" : member.id})

        if find_user is None or find_user is not None:
            new_warn = ({"id" : member.id, 
                        "user" : str(member), 
                        "reason": reason, 
                        "muted_by_name": str(ctx.message.author),
                        "muted_by_id": ctx.message.author.id
            })
            warn_db.insert(new_warn)
        
        channel = self.client.get_channel(808411931383431198)
        embed=discord.Embed(title="", description=f" ", timestamp=datetime.utcnow(), color=0xff0000
            ).set_author(name=f"{ctx.author} warned a user", icon_url=f"{ctx.author.avatar_url}"
            ).add_field(name="Warned User", value=f"{member.mention}"
            ).add_field(name="Reason", value=f"{reason}"
        )
        
        await channel.send(embed=embed)
        await ctx.channel.send(embed=embed)

        find_user =list(warn_db.find({}, {"id" : member.id}))

        if len(find_user) % 5 == 0:
            muted_role = discord.utils.get(ctx.guild.roles, id=809969441772929065)
            if muted_role in member.roles:
                return
                        
            await member.add_roles(muted_role)


    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['warns'])
    async def modlogs(self, ctx, member : discord.Member):
        '''?modlogs [member]'''
        try:
            await ctx.message.delete()
            all_warns = list(warn_db.find({"id" : member.id}))
            all_warns.reverse()
            
            if member is None or len(all_warns) == 0:
                await ctx.send("No warns found for this user!")
                return

            embed=discord.Embed(title="", description=f"All warns for {member.mention}", timestamp=datetime.utcnow(), color=0x800080)
            embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
            for index, warn in enumerate(all_warns):
                if index != 0:
                    embed.add_field(name=f'\u200b', value=f'\u200b', inline=False)
                embed.add_field(name=f'Warn {index+1} by ', value=f'<@{warn["muted_by_id"]}>', inline=True)
                embed.add_field(name=f'Reason ', value=f'{warn["reason"]}\n', inline=True)
            await ctx.send(embed=embed)
        except:
            pass
            
def setup(client):
    client.add_cog(WarnSystem(client))