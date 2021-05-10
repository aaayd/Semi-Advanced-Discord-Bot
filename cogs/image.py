from utils.constants import get_command_description
from utils.error_handler import MissingArgument
from discord.ext import commands
from discord import Embed
from animals import Animals
from datetime import datetime

class Image(commands.Cog):
    """
    Image commands to send pictures of animals.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def animal(self, ctx, name = None):
        """?animal [animal_name]"""

        if name is None:
            raise MissingArgument("Animal Name", get_command_description("animal"))

        if name == "monkey":            
            await ctx.send(embed=Embed(
                title=f"Here is a {name}, {ctx.author.display_name}", timestamp=datetime.now(), url="https://www.placemonkeys.com/512?random"
                ).set_image(url="https://www.placemonkeys.com/512?random"
                ).set_footer(text=f"{name.capitalize()} images don't have a dedicated API. Image refreshes may take a while.")
            )

        else:

            animal = Animals(str(name).lower())
            await ctx.send(embed=Embed(
                    title=f"Here is a {name}, {ctx.author.display_name}", timestamp=datetime.now(), url=animal.image()
            ).set_image(url=animal.image()
            ).set_footer(text=f"Fun fact: {str(animal.fact())}"))



def setup(bot):
    bot.add_cog(Image(bot))