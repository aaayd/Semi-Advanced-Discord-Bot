from Bot.utils.constants import command_activity_check, get_command_description, get_cluster
from Bot.utils.error_handler import MissingArgument, embed_error, embed_success, ExpectedLiteralInt
from bot import CLUSTER
import discord
from discord.ext import commands

class UtilityCommands(commands.Cog, name = "Utility Commands"):
    """
    Utility commands to keep the bot functional.
    """
    
    def __init__(self, client):
        self.client = client


    @commands.command(name="disable", description="Disable bot commands")
    @command_activity_check()
    async def _disable(self, ctx):
        f"""
        {self.client.command_prefix}{ctx.command.name}
        """

        new_activity_state = {}
        _db = get_cluster(ctx.guild.id, "CLUSTER_COMMANDS")

        commands = ctx.message.content.partition(' ')[2].split(" ")
        string = ""
        err_string = ""
        for command in commands:
            command = command.lower()
            if self.client.get_command(command) is not None and "disable" not in command and "enable" not in command:
                new_activity_state[f"dict.{command}"] = 0
                
                string += f"`{command}`, "
            else:
                err_string += f"`{command}`, "

        if  new_activity_state:
            _db.update_one({
                "id" : "type_command_activity"
                    },{
                        "$set" : new_activity_state
                    }
            )

        if err_string != "":
            await ctx.channel.send(embed=embed_error(f"Could not disable commands: {err_string[:-2]}"))
        if string != "":
            await ctx.channel.send(embed=embed_success(f"Disabled commands {string[:-2]}"))

    @commands.command(name="enable", description="Enable bot commands")
    @command_activity_check()
    async def _enable(self, ctx):
        f"""
        {self.client.command_prefix}{ctx.command.name}
        """

        new_activity_state = {}
        _db = get_cluster(ctx.guild.id, "CLUSTER_COMMANDS")

        commands = ctx.message.content.partition(' ')[2].split(" ")
        string = ""
        err_string = ""
        for command in commands:
            command = command.lower()
            if self.client.get_command(command) is not None and "disable" not in command and "enable" not in command:
                new_activity_state[f"dict.{command}"] = 1
                
                string += f"`{command}`, "
            else:
                err_string += f"`{command}`, "

        if  new_activity_state:
            _db.update_one({
                "id" : "type_command_activity"
                    },{
                        "$set" : new_activity_state
                    }
            )

        if err_string != "":
            await ctx.channel.send(embed=embed_error(f"Could not enable commands: {err_string[:-2]}"))
        if string != "":
            await ctx.channel.send(embed=embed_success(f"Enabled commands {string[:-2]}"))
        

    @commands.command(name="add_default_roles", description="Add default role for member joining")
    @command_activity_check()
    @commands.has_permissions(administrator=True)
    async def _add_default_roles(self, ctx, *, roles):
        f"""
        {self.client.command_prefix} <roles>
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

    @commands.command(name="defchannel", description="Changes default channel for selected channels")
    @command_activity_check()
    @commands.has_permissions(administrator=True)
    async def _defchannel(self, ctx, channel = None, new_channel : discord.TextChannel = None):
        """
        ?defchannel [old-channel] #[new-channel]
        """
        
        if channel is None:
            raise MissingArgument("Channel ID", get_command_description(ctx.command.name))
        
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
