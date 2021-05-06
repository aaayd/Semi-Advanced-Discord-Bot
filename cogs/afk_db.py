import discord
from discord.ext import commands
from datetime import datetime
from colorama import Fore, Style
from main import CLUSTER

afk_stat = CLUSTER["discord"]["afk"]

class AFKSystem(commands.Cog):
    def __init__(self, client):
        self.client = client
    

    @commands.command()
    async def afk(self, ctx, *, status="No status"):
        '''?afk [afk status message]'''
        await ctx.channel.trigger_typing()
        print (f"{Fore.MAGENTA}[{self.client.command_prefix}]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}]{Style.RESET_ALL} {Fore.CYAN}{ctx.author}{Style.RESET_ALL} used command {Fore.YELLOW}[AFK]{Style.RESET_ALL}")

        if "[AFK] " in ctx.author.display_name:
            return

        find_user = afk_stat.find_one({"id" : ctx.author.id})
        if find_user is None:
            greenie = ({"id" : ctx.author.id, "status": status, "date": datetime.utcnow()})
            afk_stat.insert(greenie)

            embed=discord.Embed(title="", description=f"**Status**: {status}", timestamp=datetime.utcnow(), color=0x800080
                ).set_author(name=f"{ctx.author} is now afk!", icon_url=f"{ctx.author.avatar_url}"
            )
            await ctx.channel.send(embed=embed)
        try:
            await ctx.message.author.edit(nick="[AFK] " + ctx.author.display_name)
        except:
            pass
    @commands.Cog.listener()
    async def on_message(self, message):            
        user_mentioned = False
        _ = message.content
        if "<@" and ">" in _:
            user_mentioned = True
        try:
            user_id = _.split("<@")[1]
            for word in user_id.split():
                if word[-1] == ">":
                    user_id = word[:-1]
                    if word[0] == "!":
                        user_id = user_id[1:]
                        break
                    break
                break
        except:
            pass

        try:
            if user_mentioned:
                find_user = afk_stat.find_one({"id" : int(user_id)})
            else:
                find_user = afk_stat.find_one({"id" : message.author.id})

            if find_user is None or "?afk" in message.content.lower():
                return

            if "[AFK]" in message.author.display_name:
                await message.author.edit(nick=message.author.display_name[5:])

            user_id = find_user["id"] 
            afk_status = find_user["status"]  
            afk_date = find_user["date"]
            
            elapsed_time = datetime.now() - afk_date
        
            seconds = elapsed_time.total_seconds()
            days = seconds // 86400
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            seconds = seconds % 60

            string = ""

            if days != 0.0:
                string += f"{round(days)} day" if days == 1.0 else f"{round(days)} days"

            elif hours != 0.0:
                string += f"{round(hours)} hour" if hours == 1.0 else f"{round(hours)} hours"

            elif minutes != 0.0:
                string += f"{round(minutes)} minute" if minutes == 1.0 else f"{round(minutes)} minutes"
            
            else:
                string += f"{round(seconds)} second" if hours == 1.0 else f"{round(seconds)} seconds"
            
            member_obj = await self.client.fetch_user(int(user_id))  
            if str(user_id) in message.content and message.author.id != user_id:
            
                embed=discord.Embed(title="", description=f"This user is AFK! Please wait for them to return", timestamp=datetime.utcnow(), color=0x800080
                    ).set_author(name=f"{member_obj}", icon_url=f"{member_obj.avatar_url}"
                    ).add_field(name="AFK Status", value=f"{afk_status}"
                    ).add_field(name="Time AFK", value=f"{string}"
                )
                await message.channel.send(embed=embed)
                return

            afk_stat.delete_many({"id" : message.author.id})
            

            
            embed=discord.Embed(title="", description=f"{message.author} is no longer AFK after {string}!", timestamp=datetime.utcnow(), color=0x800080
                ).set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}"
            )
            await message.channel.send(embed=embed)
    
        except:
            pass
            

            
def setup(client):
    client.add_cog(AFKSystem(client))