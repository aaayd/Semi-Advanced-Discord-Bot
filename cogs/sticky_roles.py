from utils.constants import CLUSTER_SERVER_ROLES
from main import CLUSTER
import discord
from discord.ext import commands
from discord.utils import get
from main import CLUSTER

sticks = CLUSTER["discord"]["sticky_roles"]

class StickyRole(commands.Cog):

    @commands.command()
    async def add_default_roles(self, ctx, *, roles):
        for role in roles.split():
            CLUSTER_SERVER_ROLES.update({
                "id" : "type_on_join_roles"}, 
                    {"$push" : {
                        "array" : int(role)
                    }
                })

    @commands.Cog.listener()
    async def on_member_join(self, member):
        for role_id in CLUSTER_SERVER_ROLES.find_one({"id": "type_on_join_roles"})["array"]:
            _ = discord.utils.get(member.guild.roles, id = role_id)
            
            await member.add_roles(_)
def setup(client):
    client.add_cog(StickyRole(client))