import requests
from Bot.utils.constants import command_activity_check, get_command_description
from Bot.utils.error_handler import MissingArgument
from discord.ext import commands
from discord import Embed
from animals import Animals
from datetime import datetime

class Image(commands.Cog, name="Image Commands"):
    """
    Image commands to send pictures of animals.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="meme", description="Sends random meme")
    @command_activity_check()
    async def _meme(self, ctx):
        f"""
        {self.bot.command_prefix}{ctx.command.name}
        """

        meme = requests.get("https://some-random-api.ml/meme").json()
        meme = meme["image"]

        await ctx.send(meme)

    @commands.command(name="animal", description="Sends an image of an animal")
    @command_activity_check()
    async def _animal(self, ctx, name = None):
        f"""
        {self.bot.command_prefix}{ctx.command.name} <animal_name>
        """

        if name is None:
            raise MissingArgument("Animal Name", get_command_description(ctx.command.name))

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