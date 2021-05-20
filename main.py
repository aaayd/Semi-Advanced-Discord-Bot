#!/usr/bin/env python
import os, os.path, sys, subprocess
from discord.ext import commands, ipc
from discord import Intents, Game
from colorama import Fore, Style
from discord.flags import Intents
from colorama import Fore, Style
from pymongo import MongoClient

#TODO  - Load cog
class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = "Swas")

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
        
    async def on_ipc_ready(self):
        print(f"{Fore.GREEN}[!]{Style.RESET_ALL} IPC Server is ready!")
        subprocess.Popen('python Website/website.py')

        
    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)



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
    client.load_extension(f'Bot.{folder}.{cog}')
    await ctx.send(f"Enabled Cog: {cog}")

    print(f"{Fore.GREEN}[ENABLED cog]{Style.RESET_ALL}: {cog}.py")

@client.command()
@commands.is_owner()
async def unload(ctx, folder, cog):
    client.unload_extension(f'Bot.{folder}.{cog}')
    await ctx.send(f"Disabled Cog: {cog}")

    print(f"{Fore.GREEN}[DISABLED cog]{Style.RESET_ALL}: {cog}.py")

@client.command()
@commands.is_owner()
async def update(ctx):
    await ctx.message.delete()

    for key, cogs in client.COGS.items():
        for cog in cogs:
            client.unload_extension(f'Bot.{key}.{cog}')
            try:
                client.load_extension(f'Bot.{key}.{cog}')

            except:
                print(f"{cog} failed to load" )

@client.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.message.delete()
    print (f"{Fore.BLUE}[-]{Style.RESET_ALL} Attempting bot restart")
    os.execv(sys.executable, ['python'] + sys.argv)


@client.ipc.route()
async def get_all_guilds(data):
	return client.guilds

@client.ipc.route()
async def get_guild(data):
    guild = client.get_guild(data.guild_id)
    
    if guild is None: 
        
        return None
    
    guild_data = {
		"name": guild.name,
		"id": guild.id,
        "icon_url": str(guild.icon_url),
        "member_count": int(guild.member_count),
        "role_count": int(len(guild.roles)), 
        "region": str(guild.region), 
        "owner": str(guild.owner),
        "channel_count": int(len(guild.channels)),
        "category_count": int(len(guild.categories))


	}
    try:
        return guild_data
    
    except:
        return None

for key, cogs in client.COGS.items():
    for cog in cogs:
        client.load_extension(f'Bot.{key}.{cog}')

client.ipc.start()
client.run(result["TOKEN"])
