#!/usr/bin/env python
import os, os.path, sys
from discord.ext import commands
from discord import Intents, Game
from colorama import Fore, Style
from discord.flags import Intents
from colorama import Fore, Style
from pymongo import MongoClient

#TODO  - Load cog
class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.COGS = {
            "cogs" : [
                "afk","audio","experience_system",
                "fun","image_manipulation","image","misc", 
                "logger", "moderation", "sticky_roles"
            ],
            
            "utils" : [
                "error_handler", "utility_commands", "help"
            ],


            "games" : [
                "trivia_quiz._cog", "connect_4", "battle_ships"
            ]
        }

    async def on_ready(self):
        print(f"{Fore.GREEN}[!]{Style.RESET_ALL} Bot is ready!")
        await client.change_presence(activity=Game(name=f"?help"))


from re import compile
with open('protected_vars.env') as ins:
    result = {}
    for line in ins:
        match = compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''').match(line)
        if match is not None:
            result[match.group(1)] = match.group(2)

ROOT = str(__file__)[:-len("main.py")]
CLUSTER = MongoClient(result["SRV_URL"])

client = Bot(command_prefix = ['?', '!'], intents = Intents.all(), case_insensitive=True)
client.remove_command('help')


@client.command()
@commands.is_owner()
async def load(ctx, folder, cog):
    client.load_extension(f'{folder}.{cog}')
    await ctx.send(f"Enabled Cog: {cog}")

    print(f"{Fore.GREEN}[ENABLED cog]{Style.RESET_ALL}: {cog}.py")

@client.command()
@commands.is_owner()
async def unload(ctx, folder, cog):
    client.unload_extension(f'{folder}.{cog}')
    await ctx.send(f"Disabled Cog: {cog}")

    print(f"{Fore.GREEN}[DISABLED cog]{Style.RESET_ALL}: {cog}.py")

@client.command()
@commands.is_owner()
async def update(ctx):
    await ctx.message.delete()

    for key, cogs in client.COGS.items():
        for cog in cogs:
            client.unload_extension(f'{key}.{cog}')
            try:
                client.load_extension(f'{key}.{cog}')

            except:
                print(f"{cog} failed to load" )

@client.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.message.delete()
    print (f"{Fore.BLUE}[-]{Style.RESET_ALL} Attempting bot restart")
    os.execv(sys.executable, ['python'] + sys.argv)


for key, cogs in client.COGS.items():
    for cog in cogs:
        client.load_extension(f'{key}.{cog}')

client.run(result["TOKEN"])
