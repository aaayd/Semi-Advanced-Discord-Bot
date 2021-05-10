import discord
from discord.ext import commands
from discord.errors import Forbidden


async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"May you inform the server team about this issue? :slight_smile: ", embed=embed)


class Help(commands.Cog):
    """
    Sends this help message
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # @commands.bot_has_permissions(add_reactions=True,embed_links=True)
    async def help(self, ctx, *input):
        """
        Shows all modules of that bot
        
        """
	
	
        prefix = "?"
        version = "Python 3.9.4 - Discord.py 1.7.2"
        
        owner = 257254775530323968
        owner_name = "Zenyx#0001"

        if not input:
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                description=f'Use `{prefix}help <module>` to gain more information about that module '
                                            f':smiley:\n')

            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}` {self.bot.cogs[cog].__doc__}\n'

            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            emb.add_field(name="About", value=f"The Bots is developed by {owner}, based on discord.py.\n\
                                    Please visit https://github.com/azenyx/Zenyx-Bot to submit ideas or bugs.")
            emb.set_footer(text=f"Bot is running {version}")

        elif len(input) == 1:

            for cog in self.bot.cogs:
                if cog.lower() == input[0].lower():
                    emb = discord.Embed(
                        title=f'{cog} - Commands', 
                        description=self.bot.cogs[cog].__doc__,
                        color=discord.Color.green())

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    break

            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                    color=discord.Color.orange())

        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="It's a magical place.",
                                description="I don't know how you got here. But I didn't see this coming at all.\n"
                                            "Would you please be so kind to report that issue to me on github?\n"
                                            "https://github.com/nonchris/discord-fury/issues\n"
                                            "Thank you! ~Chris",
                                color=discord.Color.red())
        await send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(Help(bot))