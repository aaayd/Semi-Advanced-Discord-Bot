from discord import Embed
from discord.ext import commands
from discord.ext.commands.errors import CommandError

def embed_error(message):
    return Embed(
        description=f":x: {message}", 
        color=0xFF0000
    )

class MissingArgument(commands.CommandError):
    def __init__(self, missing_argument, command_description, message="Missing keyword: ", ):
        self.missing_argument = f"`{missing_argument}`"
        self.command_description = f"`{command_description}`"

        self.missing_argument += f"\nCommand Usage: {self.command_description}"
        self.message = message + self.missing_argument

class MissingPermissionOnMember(commands.CommandError):
    def __init__(self, command, member, message="I have no permissions to", ):
        self.command = f"`{command}`"
        self.member = f"{member.mention}"

        self.message = f"{message} use {self.command} on {self.member}"

class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        #print(str(error))

        if isinstance(type(error), type(MissingArgument)):
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
