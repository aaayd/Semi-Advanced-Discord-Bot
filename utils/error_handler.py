from discord import Embed
from discord.ext import commands

def embed_error(message):
    return Embed(
        description=f":x: {message}", 
        color=0xFF0000
    )


class MissingArgument(Exception):
    def __init__(self, missing_argument, command_description, message="Missing keyword: ", ):
        self.missing_argument = f"`{missing_argument}`"
        self.command_description = f"`{command_description}`"

        self.missing_argument += f"\nCommand Usage: {self.command_description}"
        self.message = message + self.missing_argument

    def __str__(self):
        return self.message

class CommandErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        

        if isinstance(error, commands.CommandNotFound):
            embed = embed_error(error)
        
        else:

            error = str(error).split(":")
            error = error[2] + ": " + error[3] + ": " + error[4]
            embed = embed_error(error)
        
        await ctx.send(embed=embed)

        
def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
