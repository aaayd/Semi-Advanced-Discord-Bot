from utils.constants import get_command_description
from utils.error_handler import MissingArgument
from main import CLUSTER
import discord
from discord.ext import commands

class UtilityCommands(commands.Cog):
    """
    Utility commands to keep the bot functional.
    """
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def change_channel(self, ctx, channel = None, id = None):
        """?change_channel [channel] [new_channel_id]
        You can use `general`    or `logs` as a channel parameter 
        """
        
        if channel is None:
            raise MissingArgument("Channel ID", get_command_description("change_channel"))
        
        CLUSTER_UTIL = CLUSTER[str(ctx.message.guild.id)]["utils"]
        CLUSTER_UTIL.update({
            "id" : "type_important_channels"
            },{"$set" : {
                   f"dict.channel_{channel}" : int(id) 
                }
            })

        
def setup(client):
    client.add_cog(UtilityCommands(client))
