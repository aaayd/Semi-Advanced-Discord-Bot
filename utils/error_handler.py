from utils.constants import CHANNEL_CONFESSION_ID, CHANNEL_GENERAL_ID, CHANNEL_LOGS_ID, update_channel_id
from discord import Embed
from discord.ext import commands
from discord.ext.commands.errors import CommandError, CommandInvokeError

def embed_error(message):
    return Embed(
        description=f":x: {message}", 
        color=0xFF0000
    )

class ExpectedLiteralInt(commands.CommandError):
    def __init__(self,):
        pass

    def __str__(self):
        return "Expected `number`, not `word`"

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

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        update_channel_id(CHANNEL_GENERAL_ID, message.guild.system_channel.id)
        update_channel_id(CHANNEL_LOGS_ID, message.guild.system_channel.id)
        update_channel_id(CHANNEL_CONFESSION_ID, message.guild.system_channel.id)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #print(str(error))
        #print(type(error))

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

        await ctx.send(embed=embed)

        
def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
