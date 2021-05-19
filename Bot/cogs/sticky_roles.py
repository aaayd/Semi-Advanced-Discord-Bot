from Bot.utils.constants import get_cluster
from Bot.utils.error_handler import ExpectedLiteralInt
from main import CLUSTER
import discord
from discord.ext import commands
from discord.utils import get
from main import CLUSTER

sticks = CLUSTER["discord"]["sticky_roles"]

class StickyRole(commands.Cog):
    """
    Sticky Role related commands.
    """

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_default_roles(self, ctx, *, roles):
        try:
            [int(role) for role in roles.split()]
        except ValueError:
            raise ExpectedLiteralInt

        _db = get_cluster(ctx.message.guild.id, "CLUSTER_SERVER_ROLES")
        for role in roles.split():
            _db.update({
                "id" : "type_on_join_roles"}, 
                    {"$push" : {
                        "array" : int(role)
                    }
                })

    @commands.Cog.listener()
    async def on_member_join(self, member):
        _db = get_cluster(member.guild.id, "CLUSTER_SERVER_ROLES")
        for role_id in _db.find_one({"id": "type_on_join_roles"})["array"]:
            _ = discord.utils.get(member.guild.roles, id = role_id)
            
            await member.add_roles(_)
def setup(client):
    client.add_cog(StickyRole(client))