from Bot.utils.constants import command_activity_check, get_command_description, get_cluster
from Bot.utils.error_handler import MissingArgument, embed_success, ExpectedLiteralInt
from bot import CLUSTER
import discord
from discord.ext import commands

class UtilityCommands(commands.Cog, name = "Utility Commands"):
    """
    Utility commands to keep the bot functional.
    """
    
    def __init__(self, client):
        self.client = client


    @commands.command()
    @command_activity_check()
    async def disable(self, ctx, *, commands):
        print(commands)
        new_activity_state = {}
        _db = get_cluster(ctx.guild.id, "CLUSTER_COMMANDS")

        for command in commands:
            new_activity_state[command] = 0
         
        _db.update_one({
			"id" : "type_command_activity"
				},{
					"$set" : new_activity_state
				}
		)

        string = [f"`{command}`, " for command in commands]
        embed_success(f"Disabled commands {string}")

    @commands.command()
    @command_activity_check()
    @commands.has_permissions(administrator=True)
    async def add_default_roles(self, ctx, *, roles):
        """
        Add default role for member joining.
        ?add_default_roles [roles]
        """
        
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

    @commands.command()
    @command_activity_check()
    @commands.has_permissions(administrator=True)
    async def defchannel(self, ctx, channel = None, new_channel : discord.TextChannel = None):
        """
        Changes default channel for selected channels.
        ?defchannel [old-channel] #[new-channel]
        """
        
        if channel is None:
            raise MissingArgument("Channel ID", get_command_description("change_channel"))
        
        CLUSTER_UTIL = CLUSTER[str(ctx.message.guild.id)]["utils"]
        CLUSTER_UTIL.update({
            "id" : "type_important_channels"
            },{"$set" : {
                   f"dict.channel_{channel}" : new_channel.id
                }
            })

        embed = embed_success(f"Changed `{channel}` channel to {new_channel.mention}")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        _db = get_cluster(member.guild.id, "CLUSTER_SERVER_ROLES")
        for role_id in _db.find_one({"id": "type_on_join_roles"})["array"]:
            _ = discord.utils.get(member.guild.roles, id = role_id)
            
            await member.add_roles(_)


def setup(client):
    client.add_cog(UtilityCommands(client))
