from Bot.utils.constants import get_command_description
from Bot.utils.error_handler import MissingArgument, embed_success
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

        
def setup(client):
    client.add_cog(UtilityCommands(client))
