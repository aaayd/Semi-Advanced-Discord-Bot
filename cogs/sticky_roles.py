from main import CLUSTER
import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
from colorama import Style, Fore
from main import CLUSTER

sticks = CLUSTER["discord"]["sticky_roles"]

class StickyRole(commands.Cog):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        str = f"{Fore.YELLOW}[EVENT]{Style.RESET_ALL} {Fore.GREEN}[MEMBER JOIN]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}] {Fore.CYAN}{member}{Style.RESET_ALL}"
        find_user = sticks.find_one({"id" : member.id})
        nibble_role = discord.utils.get(member.guild.roles, id = 809888833713471488)
        colour_role = discord.utils.get(member.guild.roles, id = 813191738898251796)
        chat_lvl_rank_role = discord.utils.get(member.guild.roles, id = 813187617981333536)

        if len(member.roles) == 4:
            print(str)
            return

        try:
            await member.add_roles(nibble_role, colour_role, chat_lvl_rank_role)
            find_user["role_ids"].split(" ")
            str += f"\n{Fore.BLUE}[-] {Fore.CYAN}{member}{Style.RESET_ALL} was given roles: "

            for role_str in find_user["role_ids"].split(" "):
                try:
                    roles = get(member.guild.roles, id=int(role_str))
                    str += f"{Fore.YELLOW}{roles.name}{Style.RESET_ALL}, "
                    await member.add_roles(roles)
                except:
                    pass
        except:
            pass


        print(str)
        sticks.delete_one({"id" : member.id})

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        str = f"{Fore.YELLOW}[EVENT]{Style.RESET_ALL} {Fore.RED}[MEMBER LEAVE]{Style.RESET_ALL} {Fore.BLUE}[{datetime.now().strftime('%H:%M:%S')}] {Fore.CYAN}{member}{Style.RESET_ALL}"
        find_user = sticks.find_one({"id" : member.id})
        
        if find_user is None or len(member.roles) != 3:
            str = ""
            for role in member.roles:
                if role.id == 809888833713471488 or role.id == 813191738898251796 or role.id == 813187617981333536 or role.id == 787823476966162452 :
                    continue
                str += f"{role.id} "

            if str == "":
                return


            greenie = ({"id" : member.id, "role_ids" : str})
            sticks.insert(greenie)

def setup(client):
    client.add_cog(StickyRole(client))
