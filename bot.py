#!/usr/bin/env python
import os, os.path, sys, subprocess
from re import compile
from discord.ext import commands, ipc
from discord import Intents, Game
from colorama import Fore, Style
from discord.flags import Intents
from colorama import Fore, Style
from pymongo import MongoClient

class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = result["IPC_SECRET"])

        self.COGS = {
            "root" : [
                "website"
            ],

            "cogs" : [
                "afk","audio","experience_system",
                "fun","image_manipulation","image","misc", 
                "logger", "moderation"
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
        await bot.change_presence(activity=Game(name=f"?help"))
        
    async def on_ipc_ready(self):
        try:
            process = subprocess.Popen(f'python website.py')
        except:
            process = subprocess.Popen(["python3","website.py"])

        print(f"{Fore.GREEN}[!]{Style.RESET_ALL} IPC Server is ready!")
    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)

with open('protected_vars.env') as ins:
    result = {}
    for line in ins:
        match = compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''').match(line)
        if match is not None:
            result[match.group(1)] = match.group(2)

bot_var_arr = [result["SRV_URL"], result["TOKEN"]]
website_var_arr = [result["SECRET_KEY"], result["IPC_SECRET"], result["DISCORD_CLIENT_ID"], result["DISCORD_CLIENT_SECRET"], result["DISCORD_REDIRECT_URI"]]

ROOT = str(__file__)[:-len("bot.py")]
CLUSTER = MongoClient(result["SRV_URL"])

bot = Bot(command_prefix = '?', intents = Intents.all(), case_insensitive=True)
bot.remove_command('help')


@bot.command()
@commands.is_owner()
async def load(ctx, folder, cog):
    bot.load_extension(f'Bot.{folder}.{cog}')
    await ctx.send(f"Enabled Cog: {cog}")

    print(f"{Fore.GREEN}[ENABLED cog]{Style.RESET_ALL}: {cog}.py")

@bot.command()
@commands.is_owner()
async def unload(ctx, folder, cog):
    bot.unload_extension(f'Bot.{folder}.{cog}')
    await ctx.send(f"Disabled Cog: {cog}")

    print(f"{Fore.GREEN}[DISABLED cog]{Style.RESET_ALL}: {cog}.py")

@bot.command()
@commands.is_owner()
async def update(ctx):
    await ctx.message.delete()

    for key, cogs in bot.COGS.items():
        for cog in cogs:
            bot.unload_extension(f'Bot.{key}.{cog}')
            try:
                bot.load_extension(f'Bot.{key}.{cog}')

            except:
                print(f"{cog} failed to load" )

@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.message.delete()
    print (f"{Fore.BLUE}[-]{Style.RESET_ALL} Attempting bot restart")
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.ipc.route()
async def get_all_guilds(data):
	return bot.guilds

@bot.ipc.route()
async def get_all_commands(data):

    cmds = {}
    for command in bot.commands:
        try:
            description = str(command.help).split(".")[0]
            
            if description is not None or description != "None":
                help = str(command.help).split(".")[1]
                cmds[command.name] = [description, help]
        except:
            pass

        
        
    return cmds

@bot.ipc.route()
async def get_all_cogs(data):

    cogs = {"Games" : []}
    for cog in bot.cogs:
        cog_name = str(cog)

        if "game" in str(cog).lower():
            cog_name = "Games"
        else:
            cogs[cog_name] = []
            
        for command in bot.get_cog(cog).get_commands():
            cogs[cog_name].append([command.name, command.description])

    return dict(sorted(cogs.items(), key=lambda x: x[0].lower()))

@bot.ipc.route() 
async def get_guild(data):
    guild = bot.get_guild(data.guild_id)
    
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

for key, cogs in bot.COGS.items():
    for cog in cogs:

        string = f'Bot.{key}.{cog}'

        if key == "root":
            string = f'{cog}'

        bot.load_extension(string)

for command in bot.commands:
    print(command.name)
if __name__ == "__main__":
    if any("INSERT" in word for word in website_var_arr):
        print(f"{Fore.RED}[x]{Style.RESET_ALL} Website vars have not been set-up. Skipping...")
    else:
        bot.ipc.start()
        
    if any("INSERT" in word for word in bot_var_arr):
        print(f"{Fore.RED}[x]{Style.RESET_ALL} Bot vars have not been set-up. Skipping...")
    else:
        bot.run(result["TOKEN"])
