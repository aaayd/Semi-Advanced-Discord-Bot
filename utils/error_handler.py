from PIL import UnidentifiedImageError
from main import CLUSTER
from utils.constants     import _init_mongo_arr, _init_mongo_bool, _init_mongo_dict
from utils.constants import  COLOUR_ROLES_DICT, DEF_SNIPE_GIFS
from discord import Embed, utils
from discord.ext import commands

def embed_error(message):
    return Embed(
        description=f":x: {message}", 
        color=0xFF0000
    )

def embed_success(message):
    return Embed(
        description=f":white_check_mark: {message}", 
        color=0x66f542
    )


class ExpectedLiteralInt(commands.CommandError):
    def __init__(self,):
        pass

    def __str__(self):
        return "Expected `number`, not `word`"

class RoleNotFound(commands.CommandError):
    def __init__(self, role : str):
        self.role = role

    def __str__(self):
        return f"Role `{self.role}` not found"


class MissingArgument(commands.CommandError):
    def __init__(self, missing_argument, command_description):
        self.missing_argument = f"`{missing_argument}`"
        self.command_description = f"`{command_description}`"

    def __str__(self):
        return "Missing keyword: " + self.missing_argument + "\n" + f"Command Usage: {self.command_description}"

class MissingPermissionOnMember(commands.CommandError):
    def __init__(self, command, member):
        self.command = f"`{command}`"
        self.member = f"{member.mention}"

    def __str__(self):
        return f"I have no permissions to use {self.command} on {self.member}"

class CommandErrorHandler(commands.Cog):
    """
    Error handler for the bot - nothing interesting here.
    """
    
    def __init__(self, client):
        self.client = client
 
    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        try:
            used_channel_dict = {
                "channel_general" : guild.system_channel.id,
                "channel_logs" : guild.system_channel.id,
                "channel_confession" : guild.system_channel.id,
            }

        except:
            used_channel_dict = {
                "channel_general" : guild.text_channels[0].id,
                "channel_logs" : guild.text_channels[0].id,
                "channel_confession" : guild.text_channels[0].id,
            }

        CLUSTER_UTIL = CLUSTER[str(guild.id)]["utils"]
        _init_mongo_dict(CLUSTER_UTIL, "type_important_channels", used_channel_dict)        
        _init_mongo_arr(CLUSTER_UTIL, "type_blacklist", ["nigger"])
        _init_mongo_arr(CLUSTER_UTIL, "type_on_join_roles")
        _init_mongo_arr(CLUSTER_UTIL, "type_snipe_gifs", DEF_SNIPE_GIFS)
        _init_mongo_bool(CLUSTER_UTIL, "type_confession")

        
        for name, colour in COLOUR_ROLES_DICT.items():
            if not utils.get(guild.roles, name=name): 
                await guild.create_role(name=name, colour=colour)

        if not utils.get(guild.roles, name="Muted"): 
            await guild.create_role(name="Muted", colour=0x505050)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #print(str(error))
        #print(type(error))

        if isinstance(type(error), type(RoleNotFound)):
            embed = embed_error(str(error))


        if isinstance(type(error), type(ExpectedLiteralInt)):
            embed = embed_error(str(error))

        if isinstance(type(error), type(MissingArgument)):
            embed = embed_error(str(error))

        if isinstance(type(error), type(MissingPermissionOnMember)):
            embed = embed_error(str(error))

        if isinstance(error, commands.CommandNotFound):
            unfound_command = str(error).split(" ")[1][1:-1]
            embed = embed_error(f"Command `{unfound_command}` is unrecognised.")

        if isinstance(error, commands.MemberNotFound):
            user = str(error).split(" ")[1][1:-1]
            embed = embed_error(f"Member `{user}` not found") 

        if isinstance(type(error), type(UnidentifiedImageError)):
            pass

        await ctx.send(embed=embed)

        
def setup(client):
    client.add_cog(CommandErrorHandler(client))
